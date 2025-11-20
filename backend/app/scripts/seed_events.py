import argparse

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.services.log_generator import (
    generate_fake_events_batch,
    save_events_to_db,
)


def main():
    parser = argparse.ArgumentParser(
        description="Seed the database with fake SourceEvent logs."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=100,
        help="Number of fake events to generate (default: 100)",
    )

    args = parser.parse_args()

    # Ensure the tables exist (for now, this is enough, later we'll use Alembic)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        events = generate_fake_events_batch(args.n)
        save_events_to_db(events, db)
        print(f"Inserted {len(events)} fake events into the database.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
