from flask import request, jsonify, render_template
import datetime
from app.extensions import mongo
from app.webhook import webhook_bp

# setting IST timezone
OFFSET = datetime.timedelta(hours=5, minutes=30)

@webhook_bp.route('/')
def home():
    # return 'checking'
    return render_template('index.html')

@webhook_bp.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json  # data from webhook, in json format
        timestamp = datetime.datetime.now(datetime.timezone(OFFSET))
        
        if 'pusher' in data:
            event = {
                "author": data['pusher']['name'],
                "action": "pushed",
                "to_branch": data['ref'].split('/')[-1],
                "timestamp": timestamp.isoformat()
            }
        elif 'pull_request' in data:
            event = {
                "author": data['pull_request']['user']['login'],
                "action": "submitted a pull request",
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": timestamp.isoformat()
            }
        elif data.get('action') == 'closed':
            event = {
                "author": data['pull_request']['user']['login'],
                "action": "merged branch",
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": timestamp.isoformat()
            }
        else:
            return jsonify({"message": "Event not handled"}), 400
        
        # insert the event into mongo db
        mongo.db.events.insert_one(event)
        
        return jsonify({"message": "Event stored"}), 200

    return jsonify({"message": "unexpected Content-Type"}), 400

@webhook_bp.route('/api/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find().sort('timestamp', -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])  # ObjectId to string for json
    return jsonify(events)