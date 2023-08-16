import re
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool, cpu_count, Manager

if __name__ != "__main__":
    if os.environ.get("FLASK_ENV", "development") == "production":
        from scraping.utils import cornell_login, similarity
    else:
        from utils import cornell_login, similarity
else:
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import cornell_login, similarity

DATA_PATH = "../../data"
URL_OF_PAGE = "https://www-guidestar-org.proxy.library.cornell.edu/search"


def login(driver):
    """
    This function logs into the GuideStar website.

    Args:
        driver: A webdriver instance navigating the GuideStar website.
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
    This function searches the GuideStar website using a given search term.

    Args:
        driver: A webdriver instance navigating the GuideStar website.
        search_term: The term to be searched.

    Returns:
        A list of selenium.webdriver.remote.webelement.WebElement objects representing the search results.
    """
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Keywords"))
    )
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.ENTER)

    try:
        search_results = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "orgResults"))
        )
    except:
        return None

    return search_results


def search_website(driver, company):
    """
    This function searches the GuideStar website for a company and extracts its D-U-N-S number.

    Args:
        driver: A webdriver instance navigating the GuideStar website.
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

    if not results_table:
        print("No results found")
        return None

    # Parse the results
    soup = BeautifulSoup(results_table.get_attribute("innerHTML"), "html.parser")
    org_info_div = soup.find("div", class_="org-info my-3")

    if org_info_div:
        p_text = org_info_div.find("p").text
        ein_match = re.search(r"EIN: (\d+-\d+)", p_text)
        if ein_match:
            print("Found EIN:", ein_match.group(1))
            return ein_match.group(1)

    return None


def process_search_results(driver, company):
    ein = search_website(driver, company)
    if ein:
        company["EIN"] = ein
    else:
        company["EIN"] = None
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
        if "EIN" not in company:
            process_search_results(driver, company)
        with open(output_file_path, "w") as f:
            json.dump(companies, f, indent=4)


if __name__ == "__main__":
    # main(f"{DATA_PATH}/output.json", f"{DATA_PATH}/output.json")
    driver = webdriver.Chrome()
    search_website(driver, {"Company": "Aetna, Inc."})
