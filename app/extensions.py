from flask_pymongo import PyMongo

# Setup MongoDB here
mongo = PyMongo(uri="mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000") #replace with your mongo db url
