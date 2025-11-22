import random 
from datetime import datetime , timedelta
from typing import List , Dict , Any

from sqlalchemy.orm import Session 

from app.models import SourceEvent 


USERS = ["Alice" , "Bob" , "Charlie" , "David" , "Eve" , "Frank" , "George" , "Hannah" , "Isaac" , "James" , "Admin"]

EVENT_TYPES = [
    "login_success",
    "login_failed",
    "pull_request_opened",
    "pull_request_merged",
    "permission_changed",
    ]

def _random_ip() -> str:
    return ".".join(str(random.randint(1, 254)) for _ in range(4))



def generate_fake_events() -> Dict[str, Any]:
    user = random.choice(USERS)
    event_type = random.choice(EVENT_TYPES)

    now = datetime.utcnow()
    delta_minutes = random.randint(0, 120)
    timestamp = now - timedelta(minutes=delta_minutes)

    if event_type in("login_success" , "login_failed"):
        raw_data = {
            "ip" : _random_ip(),
            "user_agent" : random.choice(["Chrome" , "Firefox" , "Safari" , "Edge" , "Opera" , "Internet Explorer"]),
            "location" : random.choice(["USA" , "Canada" , "UK" , "Australia" , "Germany" , "France" , "Italy" , "Spain" , "Brazil" , "India" , "China" , "Japan" , "Korea" , "Russia" , "Turkey" , "Other"]),
            "success" : event_type == "login_success"
        }
    
    elif event_type in("pull_request_opened" , "pull_request_merged"):
        raw_data = {
            "repo" : random.choice(["mini-monitor" , "backend-service" , "frontend-service"]) , 
            "branch" : random.choice(["main" , "develop" , "feature/rule-engine"]) , 
            "line_changed" : random.randint(5, 500)
        }

    else:
        raw_data = {
            "old_role": random.choice(["viewer", "developer"]),
            "new_role": random.choice(["developer", "admin"]),
            "approved_by": random.choice(USERS),
        }
    
    return {
        "user": user,
        "event_type": event_type,
        "timestamp": timestamp,
        "raw_data": raw_data,
    }

def generate_fake_events_batch(n: int) -> List[Dict[str, Any]]:
    """
    Create a list of n fake events.
    """
    return [generate_fake_events() for _ in range(n)]


def save_events_to_db(events: List[Dict[str, Any]], db: Session) -> None:
    """
    Receive a list of dicts and save them as SourceEvent in the DB.
    """
    db_events = [
        SourceEvent(
            user=e["user"],
            event_type=e["event_type"],
            raw_data=e["raw_data"],
            timestamp=e["timestamp"],
        )
        for e in events
    ]

    db.add_all(db_events)
    db.commit()