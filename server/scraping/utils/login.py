import os
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from the .env file
load_dotenv(find_dotenv())


def cornell_login(driver):
    """
    This function performs login operation using the Selenium webdriver.

    It expects to be supplied with a webdriver instance as its argument
    which should already be at the login page of the website where login
    is intended.

    The function uses the Cornell NetID and password from the environment
    variables 'CORNELL_NETID' and 'CORNELL_PASSWORD'. These are expected
    to be set in the .env file at the root of the project directory.

    Args:
        driver: A webdriver instance which is already at the login page.

    """
    # Find and fill the email and the password input fields
    email_field = driver.find_element(By.ID, "username")
    email_field.clear()
    email_field.send_keys(f"{os.environ.get('CORNELL_NETID')}@cornell.edu")

    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(os.environ.get("CORNELL_PASSWORD"))

    login_button = driver.find_element(
        By.CSS_SELECTOR, 'input[name="_eventId_proceed"]'
    )
    driver.implicitly_wait(10)
    login_button.click()

    # Wait until the "trust this browser" button becomes visible and then click it
    button = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.ID, "trust-browser-button"))
    )
    button.click()

    # Implicit wait for 10 seconds for the page to load completely after login
    driver.implicitly_wait(10)
