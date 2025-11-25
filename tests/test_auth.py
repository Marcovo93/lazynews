from web.db.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={'username': 'a', 'password': 'a'})
    assert response.headers["Location"] == "/auth/login"
    
    with app.app_context():
        assert get_db().execute("SELECT * FROM users WHERE username = 'a'").fetchone() is not None