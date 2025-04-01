import pytest
from model import UserDB
from schemas import Message, Activity, Schedule, DayDetail, ActivityDetail

def test_user_creation():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    assert username in db.user_repo.users

def test_add_message():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    msg = Message(username=username, content="Hello, world!", id=None)
    message_id = db.addMessage(username, msg)
    assert message_id == 2
    assert db.getMessageHistory(username)[1].content == "Hello, world!"

def test_get_gpt_message_history():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    db.addMessage(username, Message(username=username, content="Test message"))
    messages = db.getGPTMessageHistory(username)
    assert len(messages) > 0
    assert messages[0].content == "Hello! I'm a travel planner. Where would you like to travel today?"

def test_add_activity():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    activity = Activity(
        id=None, 
        name="Visit museum", 
        short_description="Art museum visit",
        long_description="Plan to visit the art museum to see the new exhibition.",
        image_url=None
    )
    db.addActivity(username, activity)
    activities = db.getActivities(username)
    assert len(activities) == 1
    assert activities[0].name == "Visit museum"

def test_update_activity():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    activity = Activity(
        id=None, 
        name="Visit museum",
        short_description="Art museum visit",
        long_description="Plan to visit the art museum to see the new exhibition.",
        image_url=None
    )
    db.addActivity(username, activity)
    updated_activity = Activity(
        id=1, 
        name="Go to gallery",
        short_description="Gallery visit",
        long_description="Updated plan: visiting the modern art gallery",
        image_url=None
    )
    db.updateActivity(username, 1, updated_activity)
    assert db.getActivities(username)[0].name == "Go to gallery"

def test_delete_activity():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    activity = Activity(
        id=None, 
        name="Visit museum",
        short_description="Art museum visit",
        long_description="Plan to visit the art museum to see the new exhibition.",
        image_url=None
    )
    db.addActivity(username, activity)
    db.deleteActivity(username, 1)
    assert len(db.getActivities(username)) == 0

def test_add_schedule():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    schedule = Schedule(
        title="Paris Trip Itinerary",
        days=[
            DayDetail(
                day=1,
                activities=[
                    ActivityDetail(
                        name="Visit Louvre",
                        time="09:00",
                        duration="3h",
                        end_time="12:00",
                        description="Morning visit to the Louvre Museum",
                        explanations="Start with Mona Lisa exhibit"
                    )
                ]
            )
        ],
        explanations="A cultural day exploring Paris's finest art"
    )
    db.addSchedule(username, schedule)
    retrieved_schedule = db.getSchedule(username)
    assert retrieved_schedule is not None
    assert retrieved_schedule.title == "Paris Trip Itinerary"

def test_dump_gpt_messages():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    db.addMessage(username, Message(username=username, content="Test message"))
    dumped_messages = db.dumpGPTMessages(username)
    assert isinstance(dumped_messages, list)
    assert dumped_messages[0]['role'] == 'assistant'

def test_dump_activities():
    db = UserDB()
    username = "test_user"
    db.addUser(username)
    activity = Activity(
        id=None, 
        name="Visit museum",
        short_description="Art museum visit",
        long_description="Plan to visit the art museum.",
        image_url=None
    )
    db.addActivity(username, activity)
    dumped_activities = db.dumpActivities(username)
    assert isinstance(dumped_activities, dict)
    assert dumped_activities[1]['name'] == "Visit museum"

if __name__ == "__main__":
    pytest.main()
