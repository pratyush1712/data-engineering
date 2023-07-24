# Cornell Financial Data Collection

This project aims to collect financial data of all companies that have donated to Cornell in the past. To achieve this, we utilize web scraping techniques, primarily using Python and Selenium, to fetch data from various websites. The data collected includes, but is not limited to, company ticker, DUNS number, EIN, and address.

## Tools and Technologies

- Python
- Pandas
- Selenium

## Repository Structure

The project repository consists of the following directories and files:

- `processing/`: This directory is where all the data processing happens. Currently, it only has one functionality: converting Excel data of company names to JSON format.
- `scraping/`: This directory is where all the web scraping occurs.
  - `mergent_intellect/`: Contains code to scrape the Mergent Intellect website. This is currently used to get the DUNS numbers of companies.
    - `index.py`: Main script where the scraping code resides.
  - `guide_star/`: Contains code to scrape the GuideStar website. This is currently used to get the EIN of non-profit companies.
    - `index.py`: Main script where the scraping code resides.
  - `utils/`: Contains helper functions.
    - `login.py`: Contains a function `cornell_login(driver)` that will take a webdriver and log in the user through the Cornell Shibboleth authentication. It uses the NetID and password from the `.env` file.

## Setup and Usage

To use this program, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the cloned repository: `cd <repository-directory>`
3. Create a Python virtual environment to isolate the project's dependencies:
   - On Unix or MacOS, run: `python3 -m venv env`
   - On Windows, run: `py -m venv env`
4. Activate the virtual environment:
   - On Unix or MacOS, run: `source env/bin/activate`
   - On Windows, run: `.\env\Scripts\activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Create a `data` folder at the root of the project and add the Excel sheets provided by the project manager.
7. Create a `.env` file at the root of the project with the following lines:

   ```
   export CORNELL_NETID=<your-netid>
   export CORNELL_PASSWORD=<your-password>
   ```

   Replace `<your-netid>` and `<your-password>` with your Cornell NetID and password, respectively.

   To run the program, use the command `python index.py`. You can also add the `--mergent` or `--guidestar` flags to run specific scraping functionalities. If no flag is provided, the program will run both functionalities concurrently.
