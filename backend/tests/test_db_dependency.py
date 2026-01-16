from app.core import db as db_module

def test_get_db_closes_session(monkeypatch):
    class DummySession:
        def __init__(self):
            self.closed = False
        def close(self):
            self.closed = True

    dummy = DummySession()

    monkeypatch.setattr(db_module, "SessionLocal", lambda: dummy)

    gen = db_module.get_db()
    s = next(gen)
    assert s is dummy

    gen.close()
    assert dummy.closed is True
