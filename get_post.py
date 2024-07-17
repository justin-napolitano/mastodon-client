import requests
import argparse

def get_new_post(base_url, table_name):
    try:
        url = f"{base_url}/get/post"
        params = {'table': table_name}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            post = response.json()
            print("New post retrieved:")
            return post
        elif response.status_code == 404:
            print("No new posts available.")
        else:
            print(f"Failed to retrieve post: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred while fetching the post: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve a new post from the feed table.')
    parser.add_argument('--url', type=str, default="http://localhost:8080", help='Base URL for the API endpoint')
    parser.add_argument('--table', type=str, required=True, help='Table name to check against (e.g., toots)')
    args = parser.parse_args()

    get_new_post(args.url, args.table)


