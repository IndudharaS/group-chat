from app import db, Message, app

with app.app_context():
    db.session.query(Message).delete()  # Clear all rows in the Message table
    db.session.commit()
    print("Database cleared.")
