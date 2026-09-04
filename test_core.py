from core import AgentMesh, Step

def test_dag_and_audit():
    m = AgentMesh()
    m.add(Step('a', lambda x: {'v': 1}))
    m.add(Step('b', lambda x: {'v': x['a']['v'] + 1}, ['a']))
    r = m.run({})
    assert r['results']['b']['v'] == 2
    assert len(r['audit']) == 2

def test_cycle_rejected():
    m = AgentMesh()
    m.add(Step('a', lambda x: {}, ['b']))
    m.add(Step('b', lambda x: {}, ['a']))
    try:
        m.run({})
        assert False
    except ValueError:
        assert True
