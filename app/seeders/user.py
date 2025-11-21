from app.models.user import User
import bcrypt

def seed_user(db):
    password = b"1234" # Passwords should be byte strings
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    users = [
        User(username="Admin", password=hashed_password, email="admin@example.com")
    ]

    for u in users:
        exists = db.query(User).filter_by(email=u.email).first()
        if not exists:
            db.add(u)

    db.commit()
