import re
import os
import sys
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool, cpu_count, Manager

if __name__ != "__main__":
    if os.environ.get("FLASK_ENV", "development") == "production":
        from scraping.utils import cornell_login, similarity
    else:
        from utils import cornell_login, similarity
else:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import cornell_login, similarity

DATA_PATH = "../../data"
URL_OF_PAGE = (
    "https://www-capitaliq-com.proxy.library.cornell.edu/CIQDotNet/my/dashboard.aspx"
)


def login(driver):
    """
    This function logs into the GuideStar website.

    Args:
        driver: A webdriver instance navigating the GuideStar website.
    """
    try:
        cornell_login(driver)
        login(driver)
    except:
        username = os.environ["CAPITAL_IQ_USERNAME"]
        password = os.environ["CAPITAL_IQ_PASSWORD"]

        username_box = driver.find_element(By.ID, "username")
        password_box = driver.find_element(By.ID, "password")

        username_box.clear()
        password_box.clear()

        username_box.send_keys(username)
        password_box.send_keys(password)

        login_button = driver.find_element(By.ID, "myLoginButton")
        login_button.click()
        driver.implicitly_wait(10)


def search(driver, search_term):
    """
    This function searches the GuideStar website using a given search term.

    Args:
        driver: A webdriver instance navigating the GuideStar website.
        search_term: The term to be searched.

    Returns:
        A list of selenium.webdriver.remote.webelement.WebElement objects representing the search results.
    """
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "SearchTopBar"))
    )
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.ENTER)

    try:
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cTblListBody"))
        )
    except:
        return None

    return search_results


def get_ticker(driver, company, first_result_title, parent=False):
    if parent:
        driver.implicitly_wait(10)
        time.sleep(10)
    company_details = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tickersymbol"))
    )
    ticker_symbol = company_details.text.strip()
    company_name = first_result_title.text.strip()
    if similarity(company, first_result_title.text.strip(), 0.5):
        company_name = None

    tables = driver.find_elements(By.CLASS_NAME, "cTblListBody")
    location_table = tables[3]
    company_title = driver.find_element(By.ID, "CompanyHeaderInfo").text.strip()

    return {
        "Ticker": ticker_symbol,
        "Company Name": company_name,
        "Primary Location": location_table.text.strip(),
        "Parent Company": company_title if parent else None,
        "Parent": parent,
    }


def type_check(type, public):
    if public:
        return "Public Company (Operating)" == type
    return "Private Company" in type and "Operating" in type and "Subsidiary" in type


def subsidiary_ticker(driver, company_name, first_result_title):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "tickersymbol"))
    )
    tables = driver.find_elements(By.CLASS_NAME, "cTblListBody")
    parent_company_table = tables[4]
    location = tables[3].text.strip()
    parent_company_table.find_element(By.TAG_NAME, "a").click()
    parent_data = get_ticker(driver, company_name, first_result_title, True)
    if parent_data.get("Ticker") == "-":
        tables = driver.find_elements(By.CLASS_NAME, "cTblListBody")
        parent_company_table = tables[4]
        location = tables[3].text.strip()
        parent_company_table.find_element(By.TAG_NAME, "a").click()
        parent_data = subsidiary_ticker(driver, company_name, first_result_title)
    parent_data["Primary Location"] = location
    return parent_data


def parse_results(driver, results_table, company_name):
    """
    Parse the results obtained from the Capital IQ search.
    Args:
        driver: A webdriver instance navigating the Capital IQ website.
        results_table: A web element representing the search results table.
        company_name: The name of the company to be searched.
    Returns:
        A tuple containing the ticker symbol, the company name, and the location of the company.
    """
    soup = BeautifulSoup(results_table.get_attribute("innerHTML"), "html.parser")
    results = soup.find_all("tr")
    if len(results) < 1:
        print("No results found")
        return {}
    first_result_title = results[0].find("td", {"class": "NameCell"})
    first_result_type = results[0].find("td", {"class": "TypeCell"}).text.strip()
    if type_check(first_result_type, True) or type_check(first_result_type, False):
        print("Found a company")
        row = driver.find_element(By.ID, "SR0")
        row.find_element(By.CLASS_NAME, "NameCell").find_element(
            By.TAG_NAME, "a"
        ).click()
        if type_check(first_result_type, False):
            try:
                return subsidiary_ticker(driver, company_name, first_result_title)
            except Exception as e:
                print("Ran into an error: ", str(e))
                return {}
        return get_ticker(driver, company_name, first_result_title)
    else:
        print("No results found")
        return {}


def search_website(driver, company):
    """
    Searches the Capital IQ website for a company and extracts its Ticker and Primary Location.
    Args:
        driver: A webdriver instance navigating the GuideStar website.
        company: The company to be searched.
    Returns:
        A tuple containing the ticker symbol, the company name, and the location of the company.
    """
    print("Searching for", company["Company"])
    driver.get(URL_OF_PAGE)

    try:
        results_table = search(driver, company["Company"])
    except Exception as e:
        try:
            print("Login required. Attempting to log in.")
            login(driver)
            results_table = search(driver, company["Company"])
        except Exception as e:
            print("Ran into an error: ", str(e))
            return {}

    if not results_table:
        print("No results found")
        return {}

    try:
        return parse_results(driver, results_table, company["Company"])
    except Exception as e:
        print("Ran into an error: ", str(e))
        return {}


def process_search_results(driver, company):
    try:
        search_result = search_website(driver, company)
        if search_result.get("Ticker") and search_result.get("Primary Location"):
            company["Ticker"] = search_result["Ticker"]
            company["Primary Location"] = search_result["Primary Location"]
            if search_result.get("Company Name"):
                company["Ticker Company"] = search_result["Company Name"]
            else:
                company["Ticker Company"] = None
            if search_result.get("Parent"):
                company["Parent Company"] = search_result["Parent Company"]
        else:
            company["Ticker"] = None
            company["Ticker Company"] = None
            company["Primary Location"] = None
        company["Company"] = company["Company"]
    except Exception as e:
        print("Ran into an error: ", str(e))
    return company


def main(file_path, output_file_path):
    """
    This function orchestrates the scraping of the GuideStar website for companies' EIN numbers.

    Args:
        file_path: The path to the file containing the companies to be searched.
        output_file_path: The path to the file where the companies and their D-U-N-S numbers are to be saved.
    """
    # Configure the driver to run in headless mode
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome()

    with open(file_path, "r") as f:
        companies = json.load(f)

    for company in companies:
        if "Ticker" not in company or company["Ticker"] == "-":
            process_search_results(driver, company)
            with open(output_file_path, "w") as f:
                json.dump(companies, f, indent=4)


if __name__ == "__main__":
    # main(f"{DATA_PATH}/output.json", f"{DATA_PATH}/output.json")
    driver = webdriver.Chrome()
    ticker = search_website(driver, {"Company": "Disneyland"})
    print(ticker)
