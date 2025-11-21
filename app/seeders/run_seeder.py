from app.db.database import SessionLocal
from app.seeders.user import seed_user
from app.seeders.attractions import seed_attractions

def run_seeders():
    db = SessionLocal()
    try:
        seed_user(db)
        seed_attractions(db)
        print("Seeding completed successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()