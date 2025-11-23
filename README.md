# Mastodon Client

A Python-based client for interacting with Mastodon instances, supporting app registration, posting, and managing toots. This project integrates Google Cloud services for secret management and logging, facilitating robust deployment and operation.

## Features

- Register Mastodon applications with customizable scopes and redirect URIs.
- Retrieve and update posts (toots) via REST API endpoints.
- Integration with Google Cloud Secret Manager for secure credential storage.
- Google Cloud Logging integration for centralized log management.
- Dockerized for containerized deployment.

## Tech Stack

- Python 3.6+
- Mastodon.py (Mastodon API client)
- Google Cloud Secret Manager
- Google Cloud Logging
- Requests (HTTP client)
- Docker

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Google Cloud SDK installed and authenticated
- Docker (optional, for containerized usage)

### Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/justin-napolitano/mastodon-client.git
cd mastodon-client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the root directory (if needed):

```env
PROJECT_NAME=your_google_cloud_project_id
```

2. Store the following secrets in Google Cloud Secret Manager:

- `MASTODON_PASSWORD`
- `MASTODON_USERNAME`
- `MASTODON_CLIENT_ID`
- `MASTODON_SECRET`
- `MASTODON_BASE_URL`
- `MASTODON_USER_AGENT`

### Usage

Run the main scripts or utilities as needed:

- Register a Mastodon app:

```bash
python mastodon-app-registration.py --api_base_url mastodon.social
```

- Retrieve a new post:

```bash
python get_post.py --table toots --url http://localhost:8080
```

- Run the Mastodon client script (adjust URL and flags as needed):

```bash
python mastodon-client.py --url http://localhost:8080
```

### Docker Build and Push

Build and push the Docker image using the provided Cloud Build config:

```bash
gcloud builds submit --config cloudbuild.yaml .
```

## Project Structure

```
mastodon-client/
├── cloudbuild.yaml          # Google Cloud Build configuration
├── Dockerfile               # Docker image build instructions
├── gcputils/                # Google Cloud utility submodule
│   ├── GoogleCloudLogging.py
│   ├── GoogleSecretManager.py
│   ├── gcpclient.py
│   └── BigQueryClient.py
├── get_post.py              # Script to retrieve posts from API
├── mastodon-app-registration.py  # App registration utility
├── mastodon-client.py       # Main Mastodon client script
├── requirements.txt         # Python dependencies
├── readme.md                # This README file
├── sql/                    # SQL schema files
│   └── mastodon-table.sql
└── test-update-toots.sh     # Shell script for testing toot updates
```

## Future Work / Roadmap

- Expand support for more Mastodon API endpoints and features.
- Add comprehensive error handling and retry logic.
- Implement automated tests and CI/CD pipelines.
- Enhance documentation with usage examples and API references.
- Support OAuth flows with redirect URIs.
- Integrate BigQuery data analytics on stored toot data.
- Improve Docker image for production readiness.

---

For questions or contributions, please open an issue or pull request on GitHub.
