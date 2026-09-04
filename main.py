from fastapi import FastAPI
from pydantic import BaseModel
from core import AgentMesh, Step

app = FastAPI(title='AgentMesh AI')

def classify(ctx):
    text = ctx.get('text', '').lower()
    return {'intent': 'refund' if 'refund' in text else 'general'}

def plan(ctx):
    return {'actions': ['verify_order', 'draft_reply'] if ctx['classify']['intent'] == 'refund' else ['draft_reply']}

def guard(ctx):
    return {'approved': len(ctx['plan']['actions']) <= 3}

mesh = AgentMesh()
mesh.add(Step('classify', classify))
mesh.add(Step('plan', plan, ['classify']))
mesh.add(Step('guard', guard, ['plan']))

class Req(BaseModel):
    text: str

@app.post('/run')
def run(req: Req):
    return mesh.run({'text': req.text})

@app.get('/health')
def health():
    return {'ok': True, 'steps': list(mesh.steps)}
