import json
import handler

with open('request.json', 'r') as request:
    event = json.load(request)
    print(handler.face_recognition_handler(event, ''))