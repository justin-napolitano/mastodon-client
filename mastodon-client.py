import os
from mastodon import Mastodon

def register_app(client_name="cobra-bot", scopes=['read', 'write', 'follow', 'push'], redirect_uris=None, website="jnapolitano.com", to_file="masto-secret.secret", api_base_url=None, request_timeout=300, session=None, user_agent='cobra-bot'):
    '''
    Source: https://mastodonpy.readthedocs.io/en/stable/_modules/mastodon/authentication.html#Mastodon.create_app

    Create a new app with given client_name and scopes (The basic scopes are “read”, “write”, “follow” and “push” - more granular scopes are available, please refer to Mastodon documentation for which) on the instance given by api_base_url.

    Specify redirect_uris if you want users to be redirected to a certain page after authenticating in an OAuth flow. You can specify multiple URLs by passing a list. Note that if you wish to use OAuth authentication with redirects, the redirect URI must be one of the URLs specified here.

    Specify to_file to persist your app’s info to a file so you can use it in the constructor. Specify website to give a website for your app.

    Specify session with a requests.Session for it to be used instead of the default. This can be used to, amongst other things, adjust proxy or SSL certificate settings.

    Specify user_agent if you want to use a specific name as User-Agent header, otherwise “mastodonpy” will be used.

    Presently, app registration is open by default, but this is not guaranteed to be the case for all Mastodon instances in the future.

    Returns client_id and client_secret, both as strings.
    '''

    Mastodon.create_app(client_name=client_name, scopes=scopes, redirect_uris=redirect_uris, website=website, to_file=to_file, api_base_url=api_base_url, request_timeout=request_timeout, session=session, user_agent=user_agent)

if __name__ == "__main__":
    cred_file = "masto-secret.secret"
    api_base_url = "mastodon.social"
    if not os.path.exists(cred_file):
        register_app(api_base_url = api_base_url)
        print(f"App registered and credentials saved to {cred_file}")
    else:
        print(f"Credentials file '{cred_file}' already exists. Skipping app registration.")


