import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# Get the Slack Bot Token from environment variables
slack_token = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=slack_token)

# Report Links Dictionary (you can add more reports here)
reports = {
    "BW Generation (Sirf Meta)": "https://lookerstudio.google.com/reporting/7f396517-bca2-4f32-bdd4-6e3d69bc593b",
    "Sunoh (Google)": "https://lookerstudio.google.com/reporting/39b65949-427b-46b7-b005-bdb5cc8a109e",
    # Add more reports as needed
}

def send_message(channel, text):
    """Send a message to a Slack channel."""
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        print(f"Message sent: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

def capture_screenshot(report_name, date_range):
    """Capture a screenshot of the Looker Studio report."""
    if report_name not in reports:
        return f"Report '{report_name}' not found."

    # Determine the date range
    end_date = datetime.now() - timedelta(days=1)
    if date_range == "last 3 days":
        start_date = end_date - timedelta(days=3)
    elif date_range == "last 5 days":
        start_date = end_date - timedelta(days=5)
    elif date_range == "last 7 days":
        start_date = end_date - timedelta(days=7)
    else:
        return "Invalid date range."

    # Convert the dates into a format that can be used in the UI
    start_date = [start_date.day, start_date.month, start_date.year]
    end_date = [end_date.day, end_date.month, end_date.year]

    # Launch Selenium WebDriver
    driver = webdriver.Chrome()

    # Open the report URL in the browser
    report_url = reports[report_name]
    driver.get(report_url)
    time.sleep(10)  # Wait for the page to load

    try:
        # Capture the screenshot after waiting for the page to load and selecting the date range
        # Here you can add the steps for selecting the date range on the webpage

        # For demonstration purposes, we’ll just take a screenshot of the loaded page
        screenshot_path = "/tmp/screenshot.png"  # Save the screenshot temporarily
        driver.save_screenshot(screenshot_path)
        print("Screenshot taken successfully.")

        return screenshot_path
    finally:
        driver.quit()

def handle_command(event):
    """Process the Slack command and take action."""
    text = event.get('text', '')
    if "capture report" in text:
        # Extract report name and date range from the message
        parts = text.split(' ')
        if len(parts) < 4:
            send_message(event['channel'], "Invalid command format. Use: 'capture report <report_name> <date_range>'")
            return
        
        report_name = parts[2]
        date_range = parts[3]
        screenshot_path = capture_screenshot(report_name, date_range)

        if screenshot_path:
            # Upload the screenshot to Slack
            with open(screenshot_path, "rb") as file:
                try:
                    response = client.files_upload(
                        channels=event['channel'],
                        file=file,
                        filename="screenshot.png",
                        title="Looker Studio Report Screenshot"
                    )
                    print("File uploaded successfully.")
                except SlackApiError as e:
                    print(f"Error uploading file to Slack: {e.response['error']}")
        else:
            send_message(event['channel'], screenshot_path)

def listen_to_slack_events():
    """Listen for Slack events and handle commands."""
    from slack_sdk.rtm_v2 import RTMClient
    rtm = RTMClient(token=slack_token)

    @rtm.on("message")
    def handle_message(client, event):
        if 'subtype' not in event:  # Ignore bot messages
            handle_command(event)

    rtm.start()

if __name__ == "__main__":
    listen_to_slack_events()
