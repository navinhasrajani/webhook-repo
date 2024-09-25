from flask import Flask
from app.extensions import mongo
from app.webhook import webhook_bp

def create_app():
    app = Flask(__name__)

    # Set the MongoDB URI in the Flask config
    app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/github_events"  # Update with your actual MongoDB URI

    # Initialize MongoDB (from extensions.py)
    mongo.init_app(app)

    # Register the blueprint for webhook routes
    app.register_blueprint(webhook_bp)

    return app