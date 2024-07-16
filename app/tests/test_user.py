from fastapi.testclient import TestClient


# Positive case - creating a new user
def test_sign_up(client: TestClient):
    user = {
        "firstname": "Demo",
        "lastname": "User",
        "login": "DemoLogin",
        "password": "demo",
        "role": "user",
    }

    response = client.post("/user/signup", json=user)
    assert response.status_code == 200


# Negative case - creating a same user
def test_sign_up_same_user(client: TestClient):
    user = {
        "firstname": "Demo",
        "lastname": "User",
        "login": "DemoLogin",
        "password": "demo",
        "role": "user",
    }

    response = client.post("/user/signup", json=user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with login provided exists already."}


# Positive case - authenticate a user
def test_sign_in(client: TestClient):
    data = {
        "grant_type": "",
        "username": "DemoLogin",
        "password": "demo",
        "client_id": "",
        "client_secret": "",
    }

    response = client.post("/user/signin", data=data)
    assert response.status_code == 200


# Negative case - authenticate a user with wrong creds
def test_error_sign_in(client: TestClient):
    data = {
        "grant_type": "",
        "username": "DemoLogin",
        "password": "demo_demo",
        "client_id": "",
        "client_secret": "",
    }

    response = client.post("/user/signin", data=data)
    assert response.status_code == 401


# Then delete all users, just to be sure that scenarios can be redone
def test_delete_users(client: TestClient):
    response = client.delete("/user/")
    assert response.status_code == 200
    assert response.json() == {"message": "Users deleted successfully"}
