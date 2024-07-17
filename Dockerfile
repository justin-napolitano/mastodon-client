# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables for Google Cloud Logging
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/your_credentials.json

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application with the specified arguments
CMD ["python", "mastodon-app-registration.py", "--url", "https://rss-updater-pkpovjepjq-wl.a.run.app"]
