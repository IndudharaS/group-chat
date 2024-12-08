import schedule
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a Message model


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)


# Initialize the database
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        # Redirect to chat with username
        return redirect(url_for("chat", username=username))
    return render_template("index.html")


@app.route("/chat/<username>")
def chat(username):
    return render_template("chat.html", username=username)


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    new_message = Message(user=data["user"], message=data["message"])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"status": "success"})


@app.route("/get_messages")
def get_messages():
    all_messages = Message.query.all()
    messages = [{"user": msg.user, "message": msg.message}
                for msg in all_messages]
    return jsonify(messages)

# Function to clear the database


def clear_database():
    with app.app_context():
        # Clear all rows in the Message table
        db.session.query(Message).delete()
        db.session.commit()
        print(f"Database cleared at {datetime.now()}")

# Scheduler thread


def run_scheduler():
    schedule.every().day.at("16:39").do(clear_database)  # Schedule task for 12:00 AM
    while True:
        schedule.run_pending()
        time.sleep(1)


# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
