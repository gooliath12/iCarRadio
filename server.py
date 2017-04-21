import flask
from flask import Flask, request, render_template, jsonify
import requests, json, time
# import sys
# sys.path.append('functions/')   # Path to module "es_to_server.py"
application = Flask(__name__)


@application.before_request
def before_request():
    """
    This function runs at the beginning of every web request.
    (every time you enter an address in the web browser)
    """
    pass


@application.teardown_request
def teardown_request(exception):
    """
    This runs at the end of the web request.
    """
    pass


@application.route('/sns', methods = ['GET', 'POST', 'PUT'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        print "Received confirmation from AWS."
        r = requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        print "[FLASK] Received data from AWS."
        added_ts = json.loads(js['Message'])
        print json.dumps(added_ts, indent=4, sort_keys=True)
    return 'OK\n'


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    # application.run()
