from flask import Blueprint

# Define the blueprint
webhook_bp = Blueprint('webhook', __name__)

# Import routes (this will automatically associate the routes with the blueprint)
from app.webhook import routes
