import argparse
import concurrent.futures
from mergent_intellect.index import main as mergent_intellect
from guide_star.index import main as guide_star
from capital_iq.index import main as capital_iq

# Define the path to the data directory
DATA_PATH = "../data"


def add_arg(parser, flag, description):
    """
    Adds an argument to the argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which the argument should be added.
        flag (str): The flag that triggers the argument.
        description (str): A description of what the argument does.
    """
    parser.add_argument(f"--{flag}", action="store_true", help=description)


def main(type):
    """
    Parses command-line arguments and runs the appropriate functions based on those arguments.
    """
    parser = argparse.ArgumentParser(description="Run specific function.")
    add_arg(parser, "mergent", "Scrape Mergent Intellect website.")
    add_arg(parser, "guidestar", "Scrape Guidestar website.")
    add_arg(parser, "capital", "Scrape Capital IQ website.")

    args = parser.parse_args()

    # Define paths to the output files
    company_data = f"{DATA_PATH}/companies/{type}.json"
    ein_data = f"{DATA_PATH}/ein/{type}.json"
    duns_data = f"{DATA_PATH}/duns/{type}.json"
    ticker_data = f"{DATA_PATH}/ticker/{type}.json"

    # Run the appropriate function based on the provided arguments
    if args.mergent:
        mergent_intellect(company_data, duns_data)
    elif args.guidestar:
        guide_star(ein_data, ein_data)
    elif args.capital:
        capital_iq(ticker_data, ticker_data)
    else:
        # If no argument is provided, run both functions concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(mergent_intellect, company_data, duns_data)
            executor.submit(guide_star, company_data, ein_data)
            executor.submit(capital_iq, company_data, ticker_data)


def server(data):
    """
    Runs the web scrapers in parallel and returns the results.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        mergent_intellect_future = executor.submit(
            mergent_intellect, data, f"{DATA_PATH}/duns/{data}.json"
        )
        guide_star_future = executor.submit(
            guide_star, data, f"{DATA_PATH}/ein/{data}.json"
        )
        capital_iq_future = executor.submit(
            capital_iq, data, f"{DATA_PATH}/ticker/{data}.json"
        )

        return (
            mergent_intellect_future.result(),
            guide_star_future.result(),
            capital_iq_future.result(),
        )


if __name__ == "__main__":
    main("visited")
