import requests
import json

with open('secrets.json') as f:
    secrets_file = json.load(f)
client_id = secrets_file['client_id']
client_secret = secrets_file['client_secret']
bearer_token = secrets_file['bearer_token']
secret = secrets_file['secret']
base_url = secrets_file['base_url']


def get_access_token():
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    r = requests.post('https://id.twitch.tv/oauth2/token', data = data)

    global bearer_token
    bearer_token = r.json()['access_token']
    print(bearer_token)


def get_id_from_username(username):
    header = {
        'Authorization': f'Bearer {bearer_token}',
        'Client-Id': client_id
    }

    r = requests.get('https://api.twitch.tv/helix/users',
                     headers = header,
                     params = {'login': username}
                     )
    user_id = r.json()['data'][0]['id']
    return user_id


def subscribe(username, sub_type, url):
    channel_id = get_id_from_username(username)

    data = {
        "type": sub_type,
        "version": "1",
        "condition": {
            "broadcaster_user_id": channel_id
        },
        "transport": {
            "method": "webhook",
            "callback": base_url + url,
            "secret": secret
        }
    }

    header = {
        'Authorization': f'Bearer {bearer_token}',
        'Client-Id': client_id,
        'Content-Type': 'application/json'
    }

    r = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions',
                      headers = header,
                      data = json.dumps(data)
                      )

    return json.dumps(r.json(), indent = 4)


def get_subs_list():
    header = {
        'Authorization': f'Bearer {bearer_token}',
        'Client-Id': client_id
    }
    r = requests.get('https://api.twitch.tv/helix/eventsub/subscriptions',
                     headers = header)

    return json.dumps(r.json(), indent = 4)


def delete_sub(sub_id):
    header = {
        'Authorization': f'Bearer {bearer_token}',
        'Client-Id': client_id
    }
    params = {
        'id': sub_id
    }

    requests.delete('https://api.twitch.tv/helix/eventsub/subscriptions', headers = header, params = params)


def delete_all_subs():
    subs_list = json.loads(get_subs_list())['data']

    for item in subs_list:
        delete_sub(item['id'])
