import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from services.model import Message, Activity  # Ensure Activity matches the API response structure
from schemas import Schedule

client = TestClient(app)

"""Integration tests to verify API endpoints functionality"""

class TestMain:
    def setup_method(self):
        self.test_username = "test_user"

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "/index.html" in str(response.url)

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
        client = TestClient(app)
        # Add a message first to retrieve its ID
        msg = {"username": self.test_username, "content": "This is a favorite message."}
        response = client.post("/addMessage", json=msg)
        assert response.status_code == 200
        message_id = response.json()[-1]["id"]  # Assuming the last message is the one just added

        # Add the message to favorites
        response = client.post("/addToFavorites", json={"username": self.test_username, "id": message_id})
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert all(Activity(**act) for act  in response.json())

    def test_get_favorites(self):
        client = TestClient(app)
        # Add a message first to retrieve its ID
        msg = {"username": self.test_username, "content": "Wroclaw poland"}
        response = client.post("/addMessage", json=msg)
        assert response.status_code == 200
        message_id = response.json()[-1]["id"]

        # Add the message to favorites
        print(client.post("/addToFavorites", json={"username": self.test_username, "id": message_id}).json())

        # Get favorites
        response = client.get(f"/getFavorites?username={self.test_username}")
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert all(Activity(**act) for act  in response.json())

