import pytest
from fastapi.testclient import TestClient
from main import app, m
import os
client = TestClient(app)

def test_get_messages():
    # Test getting messages for a new user
    response = client.get("/getMessages", params={"username": "testuser"})
    assert response.status_code == 200

    # Add a message for the user
    message = {"username": "testuser", "content": "Hello, this is a test message"}
    response = client.post("/addMessage", json=message)
    assert response.status_code == 200

    # Get messages for the user again
    response = client.get("/getMessages", params={"username": "testuser"})
    assert response.status_code == 200
    messages = response.json()


def test_add_message():
    # Add a message for a new user
    message = {"username": "newuser", "content": "This is another test message"}
    response = client.post("/addMessage", json=message)
    assert response.status_code == 200


    # Get messages for the new user
    response = client.get("/getMessages", params={"username": "newuser"})
    assert response.status_code == 200
    messages = response.json()


def test_static_files():
    # Test serving static files
    response = client.get("/")
    if os.path.exists('frontend/dist'):
        assert response.status_code == 200
    else:
        assert response.status_code == 404