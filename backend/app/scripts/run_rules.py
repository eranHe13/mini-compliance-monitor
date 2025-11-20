from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.services.rules.rules_engine import run_rules_on_new_events


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        processed_events, created_findings = run_rules_on_new_events(db)
        print(
            f"Processed {processed_events} new events, "
            f"created {created_findings} findings."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
