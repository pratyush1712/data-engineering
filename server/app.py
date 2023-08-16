import os

os.environ["FLASK_ENV"] = "production"
import json
from flask import Flask, request, Response
from flask_cors import CORS

from scraping.capital_iq.index import process_search_results as get_ticker
from scraping.mergent_intellect.index import process_search_results as get_duns
from scraping.guide_star.index import process_search_results as get_ein

from selenium import webdriver
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
cors = CORS(
    app,
    resources={r"/api/*": {"origins": "*", "supports_credentials": True}},
)


def init_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)
    return browser


data_types = [get_ticker, get_duns, get_ein]


@app.route("/api/companies", methods=["POST"])
def process_companies_route():
    companies = request.json["companies"]

    def process_companies(companies):
        webdrivers = [init_webdriver() for _ in range(len(data_types))]

        with ThreadPoolExecutor(max_workers=3) as executor:
            for company in companies:
                futures = {
                    executor.submit(site, webdrivers[i], company): site
                    for i, site in enumerate(data_types)
                }
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        company.update(result)
                        yield json.dumps(result).encode("utf-8") + b"\n"
                    except Exception as e:
                        print("Ran into an error: ", str(e))
            yield json.dumps(companies).encode("utf-8") + b"\n"

    return Response(process_companies(companies), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
