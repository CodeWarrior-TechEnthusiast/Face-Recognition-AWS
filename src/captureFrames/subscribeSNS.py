from flask import Flask, request
import requests
import json

app = Flask(__name__)

def process_message(message):
    print(message)

@app.route('/', methods = ['GET', 'POST', 'PUT'])
def sns():
    try:
        data = json.loads(request.data)
    except:
        pass

    header = request.headers.get('x-amz-sns-message-type')
    if header == 'SubcriptionConfirmation' and 'SubscribeURL' in data:
        requests.get(data['SubscribeURL'])

    if header == 'Notification':
        process_message(data['Message'])

    return 'OK\n'

def run():
    app.run(
        host = "0.0.0.0",
        port = 5460,
        debug = True,
        use_reloader=False
    )

