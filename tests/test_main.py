import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from model import Message, Activity
from schemas import Schedule

client = TestClient(app)

"""Integration tests to verify API endpoints functionality"""

class TestMain:
    def setup_method(self):
        self.test_username = "test_user"

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == "Please access index.html"

    def test_add_message(self):
        msg = {"username": self.test_username, "content": "Hello, I need help with my travel plans."}
        response = client.post("/addMessage", json=msg)
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert any(m['content'] for m in response.json())

    def test_add_data_alternative_endpoint(self):
        msg = {"username": self.test_username, "content": "Hello, testing alternative endpoint"}
        response = client.post("/addData", json=msg)
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert any(m['content'] for m in response.json())

    def test_get_messages(self):
        # First add a message
        msg = {"username": self.test_username, "content": "Test message for retrieval"}
        client.post("/addMessage", json=msg)
        
        # Then get messages
        response = client.get(f"/getMessages?username={self.test_username}")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert any(m['content'] for m in response.json())
        assert any(m['username'] for m in response.json())

    def test_add_to_favorites(self):
        msg = {"username": self.test_username, "content": "This is a favorite message."}
        response = client.post("/addToFavorites", json={"username": self.test_username, "msg": msg})
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert any(m['content'] for m in response.json())

    def test_get_favorites(self):
        # Add a favorite first
        msg = {"username": self.test_username, "content": "Another favorite message"}
        client.post("/addToFavorites", json={"username": self.test_username, "msg": msg})
        
        # Then get favorites
        response = client.get(f"/getFavorites?username={self.test_username}")
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert any(msg['content'] for m in response.json())

    def test_remove_favorite(self):
        # Add a favorite
        msg = {"username": self.test_username, "content": "Temporary favorite message", "id": 999}
        client.post("/addToFavorites", json={"username": self.test_username, "msg": msg})
        
        # Remove the favorite
        response = client.post("/removeFavorite", json={"username": self.test_username, "msg": msg})
        assert response.status_code == 200
        assert not any(m.get('id') == 999 for m in response.json())


