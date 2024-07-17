import os
import logging
from mastodon import Mastodon
from dotenv import load_dotenv

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