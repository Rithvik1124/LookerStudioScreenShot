from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# Report Links Dictionary
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

# Allow user to select the report dynamically
selected_report_name = input("Enter the report name (e.g., 'Sunoh (Google)'): ")

if selected_report_name in reports:
    report_url = reports[selected_report_name]
else:
    print("Invalid report name. Please choose a valid report.")
    report_url = None

# Allow user to select the date range dynamically
date_range_option = input("Choose a date range (Last 3 Days, Last 5 Days, Last 7 Days, Custom Range): ").lower()

if date_range_option == "last 3 days":
    end_date = datetime.now() - timedelta(days=1)  # Yesterday
    start_date = end_date - timedelta(days=3)
elif date_range_option == "last 5 days":
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=5)
elif date_range_option == "last 7 days":
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=7)
elif date_range_option == "custom range":
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
        # Wait for the date picker button to be present in the DOM
        date_picker_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mdc-button.mat-mdc-button-base.mat-mdc-tooltip-trigger.ng2-date-picker-button.mdc-button--outlined.mat-mdc-outlined-button.mat-unthemed.canvas-date-input"))
        )
        driver.execute_script("arguments[0].click();", date_picker_button)
        time.sleep(3)  # Wait for the calendar to open

        # Start Date Selection
        start_calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.mdc-button.mat-mdc-button-base.mat-calendar-period-button'))
        )
        start_calendar_button.click()

        # Select the start month and year
        start_month = start_date[1]
        start_year = start_date[2]

        # Open the calendar's year and month view
        start_year_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'button.mat-calendar-body-cell[aria-label="{start_year}"]'))
        )
        start_year_button.click()

        start_month_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"button.mat-calendar-body-cell[aria-label='{months[start_month]} {start_year}']"))
        )
        start_month_button.click()

        time.sleep(3)

        start_day = start_date[0]
        start_day_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'button.mat-calendar-body-cell[aria-label="{start_day} {months[start_month][:3]} {start_year}"]'))
        )
        start_day_button.click()

        # END DATE SELECTION - Targeting only the end-date-picker calendar-wrapper
        end_calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.end-date-picker.calendar-wrapper .mdc-button.mat-mdc-button-base.mat-calendar-period-button'))
        )
        end_calendar_button.click()

        time.sleep(3)

        # Select the end month and year
        end_month = end_date[1]
        end_year = end_date[2]

        # Open the calendar's year and month view within the end date picker
        end_year_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{end_year}"]'))
        )
        end_year_button.click()

        end_month_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{months[end_month]} {end_year}"]'))
        )
        end_month_button.click()

        time.sleep(3)

        # Now select the end date button using aria-label for the specific date inside the end date calendar wrapper
        end_day = end_date[0]

        # Use the aria-label to find and click the correct end date button inside the end-date-picker calendar
        end_day_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{end_day} {months[end_month][:3]} {end_year}"]'))
        )
        end_day_button.click()
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.apply-button.mdc-button--unelevated'))
        )
        apply_button.click()

        time.sleep(20)  # Allow time for the page to update

    finally:
        # Capture screenshot after selecting the dates
        driver.save_screenshot("full_screenshot.png")
        print("Date selection completed and screenshot taken")
        driver.quit()
