import re
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool, cpu_count, Manager

if __name__ != "__main__":
    from scraping.utils import cornell_login, similarity
else:
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import cornell_login, similarity

# Paths to the data and the URL of the site to be scraped
DATA_PATH = "../../data"
URL_OF_PAGE = (
    "https://www-mergentintellect-com.proxy.library.cornell.edu/index.php/search/index"
)


def login(driver):
    """
    This function logs into the Mergent Intellect website.

    Args:
        driver: A webdriver instance navigating the Mergent Intellect website.
    """
    try:
        login_link = driver.find_element(By.CSS_SELECTOR, "a")
        login_link.click()
        driver.implicitly_wait(10)
    except:
        cornell_login(driver)
        login(driver)


def search(driver, search_term):
    """
    This function searches the Mergent Intellect website using a given search term.

    Args:
        driver: A webdriver instance navigating the Mergent Intellect website.
        search_term: The term to be searched.

    Returns:
        A selenium.webdriver.remote.webelement.WebElement object containing the results table.
    """
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "txtSearch"))
    )
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.submit()

    results_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "content"))
    )
    return results_table


def search_website(driver, company):
    """
    This function searches the Mergent Intellect website for a company and extracts its D-U-N-S number.

    Args:
        driver: A webdriver instance navigating the Mergent Intellect website.
        company: The company to be searched.
        companies_with_duns: A dictionary where the D-U-N-S numbers of companies are stored.
    """
    print("Searching for", company["Company"])
    driver.get(URL_OF_PAGE)
    try:
        results_table = search(driver, company["Company"])
    except:
        login(driver)
        results_table = search(driver, company["Company"])

    # parse the results
    soup = BeautifulSoup(results_table.get_attribute("innerHTML"), "html.parser")
    link = soup.find("a", {"class": "companytitle"})
    if not link:
        return (None, None)
    title = link.get("title")
    duns_match = re.search(r"D-U-N-S# ([\d-]+)", title)
    if duns_match:
        print(f"Company: {link.text}, D-U-N-S#: {duns_match.group(1)}")
        if not similarity(company["Company"], link.text, 0.5):
            return (duns_match.group(1), link.text)
        return (duns_match.group(1), None)
    else:
        print(f"Company: {link.text}, D-U-N-S#: None")
        return (None, None)


def process_search_results(driver, company):
    (duns, company_name) = search_website(driver, company)
    if duns:
        company["D-U-N-S"] = duns
        if company_name:
            company["DUNS Company"] = company_name
        else:
            company["DUNS Company"] = None
    else:
        company["D-U-N-S"] = None
        company["DUNS Company"] = None
    return company


def main(file_path, output_file_path):
    """
    This function orchestrates the scraping of the Mergent Intellect website for companies' D-U-N-S numbers.

    Args:
        file_path: The path to the file containing the companies to be searched.
        output_file_path: The path to the file where the companies and their D-U-N-S numbers are to be saved.
    """
    # configure the driver to run in headless mode
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome()

    with open(file_path, "r") as f:
        companies = json.load(f)

    for company in companies:
        process_search_results(driver, company)
        with open(output_file_path, "w") as f:
            json.dump(companies, f, indent=4)


if __name__ == "__main__":
    main(f"{DATA_PATH}/output.json", f"{DATA_PATH}/output.json")
