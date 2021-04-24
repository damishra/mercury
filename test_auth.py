from fastapi.testclient import TestClient
from mercury.main import app

client = TestClient(app)


def test_register_clean():
    response = client.post('/auth/register', json={
        "username": "sneakyturtle",
        "password": "password",
        "email": "dishant.mishra@outlook.com",
    })

    assert response.status_code == 201
    global user_id
    user_id = response.json()['id']


def test_login_clean():
    response = client.post('/auth/login', json={
        "username": "sneakyturtle",
        "password": "password",
    })

    assert response.status_code == 200


def test_update_clean():
    response = client.put(f'/auth/update/{user_id}', json={
        "username": "sneakyturtle",
        "password": "new_password",
        "email": "dishant.mishra@gmail.com",
    })

    assert response.status_code == 202


def test_delete_clean():
    response = client.delete(f'/auth/delete/{user_id}')

    assert response.status_code == 202
