import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
from PIL import Image
import os

# Function to initialize Selenium WebDriver in headless mode
def init_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--no-sandbox")
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

# Function to take a screenshot with Selenium
def capture_screenshot(start_date, end_date, driver):
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    driver.get("https://lookerstudio.google.com/u/0/reporting/d8d41df7-46a3-41ba-ab2b-0d122aa654ed/page/p_mod2aoherd")
    time.sleep(25)

    try:
        # Select start date
        date_picker_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mdc-button.mat-mdc-button-base.mat-mdc-tooltip-trigger.ng2-date-picker-button.mdc-button--outlined.mat-mdc-outlined-button.mat-unthemed.canvas-date-input"))
        )
        driver.execute_script("arguments[0].click();", date_picker_button)
        time.sleep(3)

        # Start Date Selection
        start_calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.mdc-button.mat-mdc-button-base.mat-calendar-period-button'))
        )
        start_calendar_button.click()

        start_month = start_date[1]
        start_year = start_date[2]

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

        # End Date Selection
        end_calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.end-date-picker.calendar-wrapper .mdc-button.mat-mdc-button-base.mat-calendar-period-button'))
        )
        end_calendar_button.click()

        time.sleep(3)

        end_month = end_date[1]
        end_year = end_date[2]

        end_year_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{end_year}"]'))
        )
        end_year_button.click()

        end_month_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{months[end_month]} {end_year}"]'))
        )
        end_month_button.click()

        time.sleep(3)

        end_day = end_date[0]
        end_day_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.end-date-picker.calendar-wrapper button.mat-calendar-body-cell[aria-label="{end_day} {months[end_month][:3]} {end_year}"]'))
        )
        end_day_button.click()

        # Apply button
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.apply-button.mdc-button--unelevated'))
        )
        apply_button.click()

        time.sleep(10)  # Allow time for the page to update

        # Save screenshot
        driver.save_screenshot("full_screenshot.png")

    finally:
        driver.quit()

# Streamlit interface
def main():
    st.title("Looker Studio Date Selector")

    # Hover info
    st.markdown("""
    <div style="background-color: #f1f1f1; padding: 10px; border-radius: 5px;">
        Hover over the buttons below to see how this app works. Select a date range to capture a screenshot of the dashboard.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        #### Button Functions:
        - **Last 3 Days**: Displays the data from the last 3 days.
        - **Last 5 Days**: Displays the data from the last 5 days.
        - **Last 7 Days**: Displays the data from the last 7 days.
        - **Custom Date Range**: Allows you to select a custom date range using a calendar.
        """
    )

    # Dropdown for company names
    company = st.selectbox("Select a Company", ["A", "B", "C"])

    # Buttons for last X days
    button_option = st.radio("Select Date Range", ["Last 3 Days", "Last 5 Days", "Last 7 Days", "Custom Range"])

    if button_option == "Last 3 Days":
        end_date = datetime.now() - timedelta(days=1)  # Yesterday
        start_date = end_date - timedelta(days=3)
    elif button_option == "Last 5 Days":
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=5)
    elif button_option == "Last 7 Days":
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
    else:  # Custom Range
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
        end_date = st.date_input("End Date", datetime.now() - timedelta(days=1))

    # Capture Screenshot on button click
    if st.button("Capture Screenshot"):
        driver = init_selenium()

        # Convert dates to required format
        start_date = [start_date.day, start_date.month, start_date.year]
        end_date = [end_date.day, end_date.month, end_date.year]

        # Capture the screenshot with Selenium
        capture_screenshot(start_date, end_date, driver)

        # Display image
        image = Image.open("full_screenshot.png")
        st.image(image)

        # Provide download button
        with open("full_screenshot.png", "rb") as file:
            st.download_button("Download Screenshot", file, file_name="screenshot.png", mime="image/png")

if __name__ == "__main__":
    main()
