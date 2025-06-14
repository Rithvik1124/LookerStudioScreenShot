import argparse
import os
import time
import slack_sdk
from slack_sdk.rtm_v2 import RTMClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

reports = {
    "BW Generation (Sirf Meta)": "https://lookerstudio.google.com/reporting/7f396517-bca2-4f32-bdd4-6e3d69bc593b",
    "Sunoh (Google)": "https://lookerstudio.google.com/reporting/39b65949-427b-46b7-b005-bdb5cc8a109e",
    "Healow (Google)": "https://lookerstudio.google.com/reporting/8c4d2445-2567-482c-b6e7-fe4b035c704f",
    "UA": "https://lookerstudio.google.com/reporting/ba3d152c-3c93-4dd6-a4af-f779f598a234",
    "FCC (Paid Search me Daily Report)": "https://lookerstudio.google.com/reporting/34ca31e9-0dd5-4f5e-88a5-b0c3b1dea831",
    "Scuderia": "https://lookerstudio.google.com/reporting/da8ba832-1df3-4412-9785-000262daa084",
    "Confido": "https://lookerstudio.google.com/reporting/7018b15a-0d1a-45e0-b5b1-8eb9122d66be",
    "KodeKloud": "https://lookerstudio.google.com/reporting/7c9e0649-d145-46e3-a8e5-ee09955071d7",
    "HPFY (Sirf Google)": "https://lookerstudio.google.com/reporting/8b7be612-b8b5-4acd-bccf-a520fc4da59e",
    "AOL - Intuition": "https://lookerstudio.google.com/reporting/10eac558-48e9-46eb-b5f9-1a7f0fa1e885",
    "AOL - SSSY": "https://lookerstudio.google.com/reporting/69aa7bb2-e88c-4d26-8e82-fd9bd56c5f31",
    "Cove & Lane (Sirf Meta)": "https://lookerstudio.google.com/reporting/b2ae0d43-2e1f-409e-8ea0-0a20e8e89140"
}

# Slack token and channel setup
slack_token = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=slack_token)

# Set up argparse to get user input via command-line arguments
def capture_screenshot(report_name, date_range):
    # Get the selected report URL based on user input
    if report_name in reports:
        report_url = reports[report_name]
    else:
        print("Invalid report name. Please choose a valid report.")
        return None

    # Handle date range input
    if date_range == "last 3 days":
        end_date = datetime.now() - timedelta(days=1)  # Yesterday
        start_date = end_date - timedelta(days=3)
    elif date_range == "last 5 days":
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=5)
    elif date_range == "last 7 days":
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
    elif date_range == "custom range":
        start_date_input = input("Enter start date (YYYY-MM-DD): ")
        end_date_input = input("Enter end date (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
    else:
        print("Invalid option. Defaulting to Last 3 Days.")
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=3)

    # Start and End Dates (in a list format [day, month, year])
    start_date = [start_date.day, start_date.month, start_date.year]
    end_date = [end_date.day, end_date.month, end_date.year]

    # Proceed with Selenium automation if URL is valid
    if report_url:
        # Initialize the WebDriver
        driver = webdriver.Chrome()

        # Define the months dictionary for date selection
        months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

        # Open the selected report
        driver.get(report_url)
        time.sleep(25)  # Wait for the page to load

        try:
            # Your existing code for date selection here...
            # ...

            # Capture screenshot after selecting the dates
            driver.save_screenshot("full_screenshot.png")
            print("Date selection completed and screenshot taken")
            driver.quit()

            return "full_screenshot.png"  # Return the screenshot filename
        except Exception as e:
            driver.quit()
            print(f"An error occurred: {e}")
            return None

# Slack bot event listener function
def handle_command(event):
    text = event.get('text', '')
    if "capture report" in text:
        # Parse the report_name and date_range from the Slack message
        # Example message: "capture report BW Generation (Sirf Meta) last 3 days"
        try:
            report_name, date_range = text.split(' ')[2], text.split(' ')[3]
            screenshot_path = capture_screenshot(report_name, date_range)

            if screenshot_path:
                try:
                    # Upload the screenshot to Slack
                    with open(screenshot_path, "rb") as file:
                        response = client.files_upload(
                            channels=event['channel'],
                            file=file,
                            filename="screenshot.png",
                            title="Looker Studio Report Screenshot"
                        )
                        print("File uploaded successfully")
                except SlackApiError as e:
                    print(f"Error uploading file to Slack: {e.response['error']}")
        except Exception as e:
            print(f"Error parsing command: {e}")

# Slack bot listener function
def listen_to_slack_events():
    rtm = RTMClient(token=slack_token)

    @rtm.on("message")
    def handle_message(client, event):  # Change event_data to accept 'client' and 'event'
        if 'subtype' not in event:  # Ignore bot messages
            handle_command(event)

    rtm.start()

if __name__ == "__main__":
    listen_to_slack_events()
