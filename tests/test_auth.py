from tests.utils import login

TEST_EMAIL = "test@gmail.com"


def test_auth_pages(client):
    response = client.get("/login")
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = login(client)
    assert b"Login successful." in response.data
    # Incorrect login credentials should fail.
    response = login(client, "sam", "wrongpassword")
    assert b"Wrong user ID or password." in response.data
    # Correct credentials should login
    response = login(client)
    assert b"Login successful." in response.data
