import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from model import User, Message, Activity, UserStatus

class TestUser:

    def test_initialization_default(self):
        user = User()
        assert user.username == "John Doe"
        assert len(user.message_history) == 1
        assert user.message_history[0].content == "Hello! I'm a travel planner. Where would you like to travel today?"
        assert user.status == UserStatus.DISCUSSING

    def test_initialization_custom(self):
        message_history = [Message(username="user", content="Hi there!")]
        user = User(username="Alice", message_history=message_history)
        assert user.username == "Alice"
        assert len(user.message_history) == 1
        assert user.message_history[0].content == "Hi there!"
        assert user.status == UserStatus.DISCUSSING

    def test_add_message(self):
        user = User()
        msg = Message(username="user", content="I want to travel to Paris.")
        user.addMessage(msg)
        assert len(user.message_history) == 2
        assert user.message_history[-1].content == "I want to travel to Paris."

    def test_get_message_history(self):
        user = User()
        msg = Message(username="user", content="I want to travel to Paris.")
        user.addMessage(msg)
        history = user.getMessageHistory()
        assert len(history) == 2
        assert history[-1].content == "I want to travel to Paris."

    def test_add_activity(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.")
        user.addActivity(activity, id=1)
        assert len(user.getActivities()) == 1
        assert user.getActivities()[1].name == "Sightseeing"

    def test_get_activities(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.")
        user.addActivity(activity, id=1)
        activities = user.getActivities()
        assert len(activities) == 1
        assert activities[1].name == "Sightseeing"

    def test_dump_activities(self):
        user = User()
        activity = Activity(name="Sightseeing", short_description="Visit landmarks", long_description="Visit famous landmarks in the city.")
        user.addActivity(activity, id=1)
        dumped_activities = user.dumpActivities()
        assert len(dumped_activities) == 1
        assert dumped_activities[1]['name'] == "Sightseeing"

    def test_status_management(self):
        user = User()
        user.status = UserStatus.SUMMARIZING_ACTIVITIES
        assert user.status == UserStatus.SUMMARIZING_ACTIVITIES

    def test_dump_history(self):
        user = User()
        msg = Message(username="user", content="I want to travel to Paris.")
        user.addMessage(msg)
        dumped_history = user.dumpHistory()
        assert len(dumped_history) == 2
        assert dumped_history[-1]['content'] == "I want to travel to Paris."