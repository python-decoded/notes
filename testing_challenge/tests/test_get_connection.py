import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    import os
    old = os.environ.copy()
    os.environ.setdefault("LOGIN", "")
    os.environ.setdefault("PASSWORD", "")
    yield
    os.environ.clear()
    os.environ.update(old)


@pytest.mark.parametrize("login, password", [
    ("", ""),
    ("", "pass123"),
    ("user", "")
])
def test_get_connection_error(monkeypatch, login, password):

    from tasks import get_connection
    monkeypatch.setattr(get_connection, "USER", login)
    monkeypatch.setattr(get_connection, "PASSWORD", password)

    with pytest.raises(ConnectionError):
        get_connection.get_connection()


def test_get_connection_success(monkeypatch):
    from tasks import get_connection

    monkeypatch.setattr(get_connection, "USER", "user")
    monkeypatch.setattr(get_connection, "PASSWORD", "pass123")

    get_connection.get_connection()
 