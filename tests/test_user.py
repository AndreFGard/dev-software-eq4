import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from schemas import GptMessage, Message, Activity, UserStatus
from user import User

class TestUser:

    def test_initialization_default(self):
        user = User()
        assert user.username == "John Doe"
        assert len(user.message_history) == 1
        assert user.message_history[0].content == "Hello! I'm a travel planner. Where would you like to travel today?"
        assert user.status == UserStatus.DISCUSSING
        assert user.__activities__ == {}

    def test_initialization_custom(self):
        message_history = [GptMessage(role="user", content="Hi there!", id=1)]
        user = User(username="Alice", message_history=message_history)
        assert user.username == "Alice"
        assert len(user.message_history) == 1
        assert user.message_history[0].content == "Hi there!"
        assert user.status == UserStatus.DISCUSSING

    def test_add_message(self):
        user = User()
        # Initialize the counter which is missing in the original code
        msg = Message(username="user", content="I want to travel to Paris.")
        user.addMessage(msg)
        assert len(user.message_history) == 2
        assert user.message_history[-1].content == "I want to travel to Paris."
        assert user.message_history[-1].role == "user"

    def test_add_assistant_message(self):
        user = User()
        msg = Message(username="assistant", content="I can help with Paris travel plans.")
        user.addMessage(msg)
        assert len(user.message_history) == 2
        assert user.message_history[-1].content == "I can help with Paris travel plans."
        assert user.message_history[-1].role == "assistant"

    def test_get_message_history(self):
        user = User()
        msg = Message(username="user", content="I want to travel to Paris.")
        user.addMessage(msg)
        history = user.getMessageHistory()
        assert len(history) == 2
        assert history[-1].content == "I want to travel to Paris."
        assert history[-1].username == user.username

    def test_add_activity(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.")
        user.addActivity(activity)
        assert len(user.getActivities()) == 1
        assert list(user.getActivities().values())[0].name == "Sightseeing"
        assert list(user.getActivities().keys())[0] == 1

    def test_add_activity_with_custom_id(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.", id=5)
        user.addActivity(activity)
        assert len(user.getActivities()) == 1
        assert user.getActivities()[5].name == "Sightseeing"

    def test_get_activities(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.")
        user.addActivity(activity)
        activities = user.getActivities()
        assert len(activities) == 1
        assert list(activities.values())[0].name == "Sightseeing"

    def test_add_multiple_activities(self):
        user = User()
        activity1 = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.", id=1)
        activity2 = Activity(name="Dining", short_description="Try local food", long_description="Experience local cuisine.", id=2)
        user.addActivity(activity1)
        user.addActivity(activity2)
        activities = user.getActivities()
        assert len(activities) == 2
        assert activities[1].name == "Sightseeing"
        assert activities[2].name == "Dining"

    def test_dump_activities(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.", id=1)
        user.addActivity(activity)
        dumped_activities = user.dumpActivities()
        assert len(dumped_activities) == 1
        assert dumped_activities[1]['name'] == "Sightseeing"
        assert dumped_activities[1]['short_description'] == "Visit landmarks"
        assert dumped_activities[1]['long_description'] == "Visit famous landmarks in the city."

    def test_status_management(self):
        user = User()
        user.status = UserStatus.SUMMARIZING_ACTIVITIES
        assert user.status == UserStatus.SUMMARIZING_ACTIVITIES
        user.status = UserStatus.MODIFYING_ACTIVITY
        assert user.status == UserStatus.MODIFYING_ACTIVITY

    def test_dump_history(self):
        user = User()
        msg = Message(username="user", content="I want to travel to Paris.")
        user.addMessage(msg)
        dumped_history = user.dumpHistory()
        assert len(dumped_history) == 2
        assert dumped_history[-1]['content'] == "I want to travel to Paris."
        assert dumped_history[-1]['role'] == "user"

    def test_empty_activities(self):
        user = User()
        activities = user.getActivities()
        assert len(activities) == 0
        assert user.dumpActivities() == {}