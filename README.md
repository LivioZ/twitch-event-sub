# Subscribe to Twitch Events
This is a simple way to subscribe to Twitch events and receiving notifications to a local server.

## Installation
### Install Python dependencies
```sh
virtualenv venv
source venv/bin/activate
pip install requests Flask
```
### Install ngrok
To receive Twitch notifications you need an HTTPS (on port 443) callback url. To easily have that for a local deployment you can use [ngrok](https://ngrok.com/).

ngrok creates a tunnel between a random endpoint on their domain and your local server so you don't have to expose the server to the internet by opening ports.
Register on their site and follow their instructions to install it and connect your account.

## Usage
Start ngrok tunnel with the command:
```sh
./ngrok http 5000
```
5000 should be the default port of flask when you soon will start the local server.

### Get API credentials
Follow step 1 of the Twitch API guide here: https://dev.twitch.tv/docs/api/

### Setup configuration file
Create a file named `secrets.json` in the same directory as source files with this content:
```
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "bearer_token": "your_access_token",
  "secret": "random_string",
  "base_url": "your_ngrok_base_url"
}
```
where:
* `your_client_id` is the client id created on Twitch developer console
* `your_client_secret` is the client secret created on Twitch developer console
* `your_access_token` is the token returned by the function `get_access_token()`
  * run:
    ```
    python client.py
    import client
    client.get_access_token()
    ```
  * copy the returned value and paste it in the file
* `secret` is random string between 10 and 100 characters, create it with a password manager
* `base_url` is the HTTPS url where twitch will send requests, use the one that's written in the ngrok console near `forwarding` keyword (make sure to copy the HTTPS one)

### Run the local server
Type in a terminal:
```sh
source venv/bin/activate
python server.py
```

### Subscribe to Twitch events
Open another terminal and type:
```sh
source venv/bin/activate
python client.py
import client
client.subscribe(username, sub_type, url)
```
where:
* `username` is the streamer name
* `sub_type` is the subscription type, choose one from [Twitch Subscription Types](https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types)
* `url` is the route on the local server which will handle this sub type, for example to send to `/twitch/update/` route, put the string `'/twitch/update/'` in the field. You can create a new route by copying another and adapting it for the new subscription type.

### Other
You can use the `client.delete_sub` function to unsubscribe from an event and the `client.get_subs_list` to get a list of subscriptions.

If your restart ngrok and/or the server `client_id`, `client_secret`, `bearer_token` and `base_url` could have changed, if that's the case change them in the `secrets.json` file.

You can connect the server with other applications, like a bot that send notifications in discord or somewhere else, that's up to you.