from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List
import time, uuid

@dataclass
class Step:
    name: str
    fn: Callable[[dict], dict]
    depends_on: List[str] = field(default_factory=list)
    retries: int = 2
    timeout_s: float = 5.0

class AgentMesh:
    def __init__(self):
        self.steps: Dict[str, Step] = {}
        self.audit: List[dict] = []
        self.failures: Dict[str, int] = {}

    def add(self, step: Step):
        if step.name in self.steps:
            raise ValueError('duplicate step')
        self.steps[step.name] = step

    def _order(self):
        result, temp, perm = [], set(), set()
        def visit(n):
            if n in perm:
                return
            if n in temp:
                raise ValueError('cycle detected')
            temp.add(n)
            for d in self.steps[n].depends_on:
                if d not in self.steps:
                    raise ValueError(f'missing dependency {d}')
                visit(d)
            temp.remove(n)
            perm.add(n)
            result.append(n)
        for n in self.steps:
            visit(n)
        return result

    def run(self, payload: dict):
        run_id = str(uuid.uuid4())
        state, completed = dict(payload), {}
        for name in self._order():
            step = self.steps[name]
            if self.failures.get(name, 0) >= 3:
                self.audit.append({'run_id': run_id, 'step': name, 'status': 'circuit_open'})
                continue
            last_err = None
            for attempt in range(step.retries + 1):
                started = time.time()
                try:
                    out = step.fn({**state, **completed})
                    if time.time() - started > step.timeout_s:
                        raise TimeoutError(name)
                    completed[name] = out
                    self.audit.append({'run_id': run_id, 'step': name, 'status': 'ok', 'attempt': attempt + 1})
                    self.failures[name] = 0
                    break
                except Exception as exc:
                    last_err = str(exc)
                    self.failures[name] = self.failures.get(name, 0) + 1
                    self.audit.append({'run_id': run_id, 'step': name, 'status': 'error', 'attempt': attempt + 1, 'error': last_err})
            else:
                completed[name] = {'error': last_err}
        return {'run_id': run_id, 'results': completed, 'audit': self.audit}
