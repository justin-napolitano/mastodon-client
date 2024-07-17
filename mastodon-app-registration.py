import os
import logging
from mastodon import Mastodon
from dotenv import load_dotenv
import requests
import json
from datetime import datetime


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app(app_name="cobra-bot2", api_base_url=None, to_file="masto-secret.secret"):
    '''
    Source: https://mastodonpy.readthedocs.io/en/stable/_modules/mastodon/authentication.html#Mastodon.create_app

    Create a new app with given app_name and scopes (The basic scopes are “read”, “write”, “follow” and “push” - more granular scopes are available, please refer to Mastodon documentation for which) on the instance given by api_base_url.

    Specify redirect_uris if you want users to be redirected to a certain page after authenticating in an OAuth flow. You can specify multiple URLs by passing a list. Note that if you wish to use OAuth authentication with redirects, the redirect URI must be one of the URLs specified here.

    Specify to_file to persist your app’s info to a file so you can use it in the constructor. Specify website to give a website for your app.

    Specify session with a requests.Session for it to be used instead of the default. This can be used to, amongst other things, adjust proxy or SSL certificate settings.

    Specify user_agent if you want to use a specific name as User-Agent header, otherwise “mastodonpy” will be used.

    Presently, app registration is open by default, but this is not guaranteed to be the case for all Mastodon instances in the future.

    Returns client_id and client_secret, both as strings.
    '''

    Mastodon.create_app(
        client_name=app_name,
        scopes=['read', 'write', 'follow', 'push'],
        api_base_url=api_base_url,
        to_file=to_file,
        website="https://jnapolitano.com"
    )
    logging.info(f"App '{app_name}' registered and credentials saved to '{to_file}'")


def format_datetime_for_api(dt):
    if dt:
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    return None

def update_toot(data, base_url):
    try:
        url = f"{base_url}/update/toots"
        headers = {'Content-Type': 'application/json'}
        
        toot_data = {
            "id": data['id'],
            "created_at": format_datetime_for_api(data['created_at']),
            "in_reply_to_id": data.get('in_reply_to_id'),
            "in_reply_to_account_id": data.get('in_reply_to_account_id'),
            "sensitive": data.get('sensitive', False),
            "spoiler_text": data.get('spoiler_text', ''),
            "visibility": data.get('visibility', 'public'),
            "language": data.get('language', ''),
            "uri": data.get('uri'),
            "url": data.get('url'),
            "site_url": data['account']['url'] if 'account' in data and 'url' in data['account'] else '',
            "replies_count": data.get('replies_count', 0),
            "reblogs_count": data.get('reblogs_count', 0),
            "favourites_count": data.get('favourites_count', 0),
            "favourited": data.get('favourited', False),
            "reblogged": data.get('reblogged', False),
            "muted": data.get('muted', False),
            "bookmarked": data.get('bookmarked', False),
            "pinned": data.get('pinned', False),
            "content": data.get('content', ''),
            "filtered": json.dumps(data.get('filtered', [])),
            "reblog": json.dumps(data.get('reblog')),
            "application": json.dumps(data.get('application')),
            "account": json.dumps(data.get('account')),
            "media_attachments": json.dumps(data.get('media_attachments', [])),
            "mentions": json.dumps(data.get('mentions', [])),
            "tags": json.dumps(data.get('tags', [])),
            "emojis": json.dumps(data.get('emojis', [])),
            "card": json.dumps(data.get('card')),
            "poll": json.dumps(data.get('poll'))
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(toot_data))
        if response.status_code == 201:
            print(f"Successfully added toot: {toot_data['id']}")
        elif response.status_code == 200:
            print(f"Toot updated or no update needed for: {toot_data['id']}")
        else:
            print(f"Failed to update toot: {toot_data['id']}, Status Code: {response.status_code}, Message: {response.text}")
    except Exception as e:
        print(f"An error occurred while updating the toot: {e}")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    cred_file = "masto-secret.secret"
    password = os.getenv("MASTODON_PASSWORD")
    username = os.getenv("MASTODON_USERNAME")
    api_base_url = "https://mastodon.social"
    user_cred_file = 'cobra-usercred.secret'

    if not os.path.exists(cred_file):
        logging.info("Credentials file not found. Registering app...")
        create_app(api_base_url=api_base_url, to_file=cred_file)
    else:
        logging.info(f"Credentials file '{cred_file}' already exists. Skipping app registration.")

    # Instantiate the App
    mastodon = Mastodon(
        client_id=cred_file,
        api_base_url=api_base_url
    )
    logging.info("Mastodon app instance created")

    # Login with .env credentials
    try:
        mastodon.log_in(
            username,
            password,
            to_file=user_cred_file
        )
        logging.info("Logged in and user credentials saved")
    except Exception as e:
        logging.error(f"Error during login: {e}")

    # Run a session
    mastodon = Mastodon(
        client_id=cred_file,
        access_token=user_cred_file,
        api_base_url=api_base_url
    )
    logging.info("Mastodon session started")

    #test a toot

    mastodon.toot('Tooting from Python using cobrabot !')

    data = mastodon.toot('Tooting from Python using cobrabot !')

    print(data)