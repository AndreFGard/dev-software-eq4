import pytest
from fastapi.testclient import TestClient
from main import app
from model import Message

client = TestClient(app)

"""This is an integration test class which verifies that
 the message storing and getting is working properly"""

global message_counter

class TestMain:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == "Please access index.html"

    def test_add_data(self):
        msg = {"username": "test_user", "content": "Hello, I need help with my travel plans."}
        response = client.post("/addData", json=msg)
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[1]['content'] == "Hello, I need help with my travel plans."

    def test_add_data2(self):
        msg = {"username": "test_user", "content": "Hello, mesage2"}
        response = client.post("/addData", json=msg)
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[-2]['content'] == msg['content']

    def test_get_messages_after_add(self):
        username = "test_user"
        msg = {"username": username, "content": "Hello, mesage3"}
        response = client.post("/addData", json=msg)
        assert response.status_code == 200
        response = client.get(f"/getMessages?username={username}")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[-2]['content'] == msg['content']

    def test_get_messages_username(self):
        username = "test_user"
        response = client.get(f"/getMessages?username={username}")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[-2]['username'] == username

    def test_add_to_favorites(self):
        username = "test_user"
        msg = {"username": "test_user", "content": "This is a favorite message."}
        response = client.post("/addToFavorites", json={"username": username, "msg": msg})
        assert response.status_code == 200
        
        assert len(response.json()) > 0
        assert response.json()[-1]['content'] == "This is a favorite message."