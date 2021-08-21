import json
import hmac
import hashlib
from flask import Flask, request, abort

app = Flask(__name__)


def verify_signature(r):
    with open('secrets.json') as f:
        secret = json.load(f)['secret']
    body = r.get_data(True, True, False)
    message = f"{r.headers['Twitch-Eventsub-Message-Id']}{r.headers['Twitch-Eventsub-Message-Timestamp']}{body}"
    expected_signature = f"sha256={hmac.new(bytes(secret, 'utf-8'), msg = bytes(message, 'utf-8'), digestmod = hashlib.sha256).hexdigest()}"
    request_signature = r.headers['Twitch-Eventsub-Message-Signature']
    return expected_signature == request_signature


def respond_to_challenge(r):
    print(json.dumps(r.json, indent = 4))
    challenge = r.json['challenge']

    if not verify_signature(r):
        abort(412)
    else:
        streamer_id = r.json['subscription']['condition']['broadcaster_user_id']
        sub_type = r.json['subscription']['type']

        print(f'Responded to a challenge for subscription type: {sub_type} for streamer id: {streamer_id}')

        return challenge


@app.route("/twitch/update/", methods = ['POST'])
def twitch_update():
    try:
        return respond_to_challenge(request)
    except KeyError:
        streamer_name = request.json['event']['broadcaster_user_name']
        title = request.json['event']['title']
        category = request.json['event']['category_name']

        message = f'{streamer_name} updated stream information:\nTitle: {title}\nCategory{category}'

        print(message)

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/twitch/online/", methods = ['POST'])
def twitch_online():
    try:
        return respond_to_challenge(request)
    except KeyError:
        streamer_name = request.json['event']['broadcaster_user_name']

        message = f'{streamer_name} started a livestream'

        print(message)

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/twitch/offline/", methods = ['POST'])
def twitch_offline():
    try:
        return respond_to_challenge(request)
    except KeyError:
        streamer_name = request.json['event']['broadcaster_user_name']

        message = f'{streamer_name} ended the livestream'

        print(message)

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
