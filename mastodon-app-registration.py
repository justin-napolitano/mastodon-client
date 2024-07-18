import os
import logging
from mastodon import Mastodon
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import argparse
from google.cloud import secretmanager
from gcputils.GoogleCloudLogging import GoogleCloudLogging
from gcputils.GoogleSecretManager import GoogleSecretManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app(app_name="cobra-bot2", api_base_url=None, to_file="masto-secret.secret"):
    '''
    Create a new app with given app_name and scopes on the instance given by api_base_url.

    Args:
    app_name (str): Name of the app to be created.
    api_base_url (str): Base URL of the Mastodon instance.
    to_file (str): File to save the app credentials.

    Returns:
    None
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
    '''
    Format datetime for API.

    Args:
    dt (datetime): Datetime object to format.

    Returns:
    str: Formatted datetime string.
    '''
    if dt:
        formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
        logging.debug(f"Formatted datetime: {formatted_date}")
        return formatted_date
    return None

def update_toot(data, base_url):
    '''
    Update toot in the database by sending a POST request to the API endpoint.

    Args:
    data (dict): Toot data dictionary.
    base_url (str): Base URL of the API endpoint.

    Returns:
    None
    '''
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
            "site_url": data['site_url'],
            # data['account']['url'] if 'account' in data and 'url' in data['account'] else '',
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
        
        logging.debug(f"Toot data: {json.dumps(toot_data, indent=4)}")
        response = requests.post(url, headers=headers, data=json.dumps(toot_data))
        if response.status_code == 201:
            logging.info(f"Successfully added toot: {toot_data['url']}")
        elif response.status_code == 200:
            logging.info(f"Toot updated or no update needed for: {toot_data['url']}")
        else:
            logging.error(f"Failed to update toot: {toot_data['id']}, Status Code: {response.status_code}, Message: {response.text}")
    except Exception as e:
        logging.exception(f"An error occurred while updating the toot: {e}")

def get_new_post(base_url, table_name):
    '''
    Retrieve a new post from the specified table by sending a GET request to the API endpoint.

    Args:
    base_url (str): Base URL of the API endpoint.
    table_name (str): Name of the table to retrieve the post from.

    Returns:
    dict: Retrieved post data.
    '''
    try:
        url = f"{base_url}/get/post"
        params = {'table': table_name}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            post = response.json()
            logging.info("New post retrieved")
            return post
        elif response.status_code == 404:
            logging.info("No new posts available")
        else:
            logging.error(f"Failed to retrieve post: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"An error occurred while fetching the post: {e}")

def format_a_toot(post):
    '''
    Format a toot message from the post data.

    Args:
    post (dict): Post data dictionary.

    Returns:
    str: Formatted toot message.
    '''
    toot = f"New post : {post['title']} \n {post['guid']}"  
    logging.debug(f"Formatted toot: {toot}")
    return toot

def format_datetime(date_str, date_format="%a, %d %b %Y %H:%M:%S %z"):
    '''
    Format a date string to a specified format.

    Args:
    date_str (str): Date string to format.
    date_format (str): Format of the date string.

    Returns:
    str: Formatted date string.
    '''
    try:
        dt = datetime.strptime(date_str, date_format)
        formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S")
        logging.debug(f"Formatted datetime: {formatted_date}")
        return formatted_date
    except Exception as e:
        logging.error(f"An error occurred while formatting date: {e}")
        return None

def pretty_print_json(data):
    '''
    Pretty print a JSON object.

    Args:
    data (dict): JSON data to print.

    Returns:
    None
    '''
    logging.debug(json.dumps(data, indent=4))

def print_directory_contents(directory):
    for root, dirs, files in os.walk(directory):
        logging.info(f"Root: {root}")
        for dir_name in dirs:
            logging.info(f"Directory: {os.path.join(root, dir_name)}")
        for file_name in files:
            logging.info(f"File: {os.path.join(root, file_name)}")

def access_secret_version(client, secret_id, version_id='latest'):
    """
    Access the secret version and return the payload.

    Args:
    client: The Secret Manager client.
    secret_id: The ID of the secret to access.
    version_id: The version of the secret to access (default is 'latest').

    Returns:
    The secret payload as a string.
    """
    name = f"projects/{client.project}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode("UTF-8")
    return payload

if __name__ == "__main__":
    # load_dotenv()  # Load environment variables from .env file

    parser = argparse.ArgumentParser(description='Retrieve a new post from the feed table.')
    parser.add_argument('--url', type=str, default="http://localhost:8080", help='Base URL for the API endpoint')
    parser.add_argument('--local', action='store_true', help='Use local credentials for Google Cloud Logging')
    args = parser.parse_args()
    
    toot_table = "toots"
    base_url = args.url

    # Setup Google Cloud Logging
    # project_id = os.environ.get("PROJECT_NAME")
    # credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") if args.local else None
    # gcl = GoogleCloudLogging(project_id, credentials_path)
    # gcl.setup_logging()

    # cred_file = "/app/masto-secret.secret"
    
    # logging.info(cred_file)
    # logging.info(os.getcwd())
    # print_directory_contents(os.getcwd())

    #Mastodon CLIENT ID FROM SECRET MANSGER

    # project_id = os.getenv("PROJECT_NAME")
    project_id = "smart-axis-421517"
    gsm = GoogleSecretManager(project_id)
    # client.project = project_id

    try:
        mastodon_password = gsm.access_secret("MASTODON_PASSWORD")
        mastodon_username = gsm.access_secret("MASTODON_USERNAME")
        mastodon_client_id = gsm.access_secret("MASTODON_CLIENT_ID")
        mastodon_secret = gsm.access_secret("MASTODON_SECRET")
        mastodon_base_url = gsm.access_secret("MASTODON_BASE_URL")
        mastodon_user_agent = gsm.access_secret("MASTODON_USER_AGENT")
        logging.info("Secrets accessed successfully")
    except Exception as e:
        logging.error(f"Error accessing secrets: {e}")
        raise

    # api_base_url = "https://mastodon.social"
    # user_cred_file = '/app/cobra-usercred.secret'

    # if not os.path.exists(cred_file):
    #     logging.info("Credentials file not found. Registering app...")
    #     create_app(api_base_url=api_base_url, to_file=cred_file)
    # else:
    #     logging.info(f"Credentials file '{cred_file}' already exists. Skipping app registration.")

    # Instantiate the App
    mastodon = Mastodon(
        client_id=mastodon_client_id,
        client_secret=mastodon_secret,
        api_base_url=mastodon_base_url,
        user_agent=mastodon_user_agent
    )
    logging.info("Mastodon app instance created")

    # Login with secrets
    try:
        user_access_token = mastodon.log_in(
            mastodon_username,
            mastodon_password,
            # to_file=user_cred_file
        )
        logging.info("Logged in and user credentials saved")
    except Exception as e:
        logging.error(f"Error during login: {e}")

    # Run a session
    mastodon = Mastodon(
        client_id=mastodon_client_id,
        client_secret=mastodon_secret,
        access_token=user_access_token,
        api_base_url=mastodon_base_url
    )
    logging.info("Mastodon session started")

    # Test a toot
    post = get_new_post(base_url=base_url, table_name=toot_table)
    logging.info(f"post information: {post}")
    if post:
        toot = format_a_toot(post)
        toot_result = mastodon.toot(toot)

        # Add empty application and account fields
        toot_result["application"] = {}
        toot_result["account"] = {}
        toot_result["site_url"] =post['link']

        update_toot(data=toot_result, base_url=base_url)
    else:
        logging.info("No new post to toot")
