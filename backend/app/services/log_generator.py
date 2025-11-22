import random 
from datetime import datetime , timedelta
from typing import List , Dict , Any

from sqlalchemy.orm import Session 

from app.models import SourceEvent 


USERS = ["Alice" , "Bob" , "Charlie" , "David" , "Eve" , "Frank" , "George" , "Hannah" , "Isaac" , "James" , "Admin"]

EVENT_TYPES = [
    # Auth
    "login_success",
    "login_failed",
    "mfa_challenge",
    "mfa_failed",
    "mfa_success",
    # Code / Git
    "pull_request_opened",
    "pull_request_merged",
    # Access / Permissions
    "permission_changed",
    "api_token_created",
    "api_token_revoked",
    # Deployments / CI
    "deployment_started",
    "deployment_succeeded",
    "deployment_failed",
    # Storage / Buckets
    "storage_bucket_created",
    "storage_bucket_permission_changed",
]

def _random_ip() -> str:
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def _random_timestamp(days_back: int = 30) -> datetime:
    """
    Return a random timestamp within the last N days.
    """
    now = datetime.utcnow()
    delta_days = random.randint(0, days_back)
    delta_hours = random.randint(0, 23)
    delta_minutes = random.randint(0, 59)
    return now - timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)

def _random_env() -> str:
    return random.choice(["dev", "staging", "prod"])

def _random_service() -> str:
    return random.choice(["auth-service", "billing-api", "frontend-app", "mini-monitor"])


def generate_fake_events() -> Dict[str, Any]:
    user = random.choice(USERS)
    event_type = random.choice(EVENT_TYPES)
    timestamp = _random_timestamp(days_back=30)


    if event_type in("login_success" , "login_failed"):
        raw_data = {
            "ip" : _random_ip(),
            "user_agent" : random.choice(["Chrome" , "Firefox" , "Safari" , "Edge" , "Opera" , "Internet Explorer"]),
            "location" : random.choice(["USA" , "Canada" , "UK" , "Australia" , "Germany" , "France" , "Italy" , "Spain" , "Brazil" , "India" , "China" , "Japan" , "Korea" , "Russia" , "Turkey" , "Other"]),
            "success" : event_type == "login_success"
        }
    
    elif event_type in ("mfa_challenge", "mfa_failed", "mfa_success"):
        raw_data = {
            "ip": _random_ip(),
            "location": random.choice(
                ["USA", "Germany", "India", "Brazil", "Other"]
            ),
            "method": random.choice(["totp", "sms", "push"]),
            "device_trusted": random.choice([True, False]),
            "success": event_type == "mfa_success",
        }

# --------- Git / PR events ---------    
    elif event_type in ("pull_request_opened", "pull_request_merged"):
        raw_data = {
            "repo": random.choice(
                ["mini-monitor", "backend-service", "frontend-service"]
            ),
            "branch": random.choice(["main", "develop", "feature/rule-engine"]),
            "lines_changed": random.randint(5, 500),
            "approved_by": random.choice(USERS + [None]),
        }

# --------- Permissions / API tokens ---------
    elif event_type == "permission_changed":
        raw_data = {
            "old_role": random.choice(["viewer", "developer"]),
            "new_role": random.choice(["developer", "admin"]),
            "approved_by": random.choice(USERS + [None]),
        }

# --------- API tokens ---------
    elif event_type == "api_token_created":
        has_expiry = random.choice([True, False])
        scopes_options = [
            ["read:repos"],
            ["read:repos", "write:deploy"],
            ["admin:*"],
        ]
        scopes = random.choice(scopes_options)
        raw_data = {
            "token_id": f"tok_{random.randint(1000, 9999)}",
            "scopes": scopes,
            "created_by": user,
            "has_expiry": has_expiry,
            "expires_at": (
                (datetime.utcnow() + timedelta(days=random.randint(1, 365))).isoformat()
                if has_expiry
                else None
            ),
        }

    elif event_type == "api_token_revoked":
        raw_data = {
            "token_id": f"tok_{random.randint(1000, 9999)}",
            "revoked_by": user,
        }

# --------- Deployments ---------
    elif event_type in (
        "deployment_started",
        "deployment_succeeded",
        "deployment_failed",
    ):
        raw_data = {
            "service": _random_service(),
            "environment": _random_env(),
            "version": f"v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
            "initiated_by": random.choice(["CI", user]),
        }

# --------- Storage / Buckets ---------
    elif event_type == "storage_bucket_created":
        public = random.choice([True, False])
        raw_data = {
            "bucket_name": random.choice(
                ["logs-archive-2024", "user-uploads", "backups", "analytics-data"]
            ),
            "public": public,
            "region": random.choice(["eu-west-1", "us-east-1", "ap-south-1"]),
        }

    elif event_type == "storage_bucket_permission_changed":
        public = random.choice([True, False])
        raw_data = {
            "bucket_name": random.choice(
                ["logs-archive-2024", "user-uploads", "backups", "analytics-data"]
            ),
            "public": public,
            "changed_by": user,
        }

# --------- Fallback ---------
    else:
        raw_data = {
            "message": "Unknown event type",
        }

    return {
        "user": user,
        "event_type": event_type,
        "timestamp": timestamp,
        "raw_data": raw_data,
    }



def generate_fake_events_batch(n: int) -> List[Dict[str, Any]]:
    return [generate_fake_events() for _ in range(n)]


def save_events_to_db(events: List[Dict[str, Any]], db: Session) -> None:
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