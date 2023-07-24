import os
import pandas as pd
import json
import argparse

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


def convert_excel_to_json(path_to_excel_file):
    xls = pd.ExcelFile(path_to_excel_file)
    sheet_names = xls.sheet_names
    output_folder = os.path.splitext(path_to_excel_file)[0] + "_json"
    os.makedirs(output_folder, exist_ok=True)

    for sheet_name in sheet_names:
        df = xls.parse(sheet_name)
        output_json_file = os.path.join(output_folder, f"{sheet_name}.json")
        df.to_json(output_json_file, orient="records")


def convert_to_excel(path_to_json_file, output_path, sheet_name):
    # Create a DataFrame from the array of dictionaries
    with open(path_to_json_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    null_rows = df[df.iloc[:, 1:].isnull().all(axis=1)]

    # Exclude rows where the company name is also null
    null_rows = null_rows.dropna(subset=["Company"])

    # Get the count of null rows
    num_null_rows = len(null_rows)
    print(f"Number of null rows: {num_null_rows}")
    with pd.ExcelWriter(
        output_path, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    # writer = pd.ExcelWriter(output_path, engine="openpyxl")
    # df.to_excel(output_path, sheet_name=sheet_name, index=False)
    # Write the DataFrame to an Excel file


def merge_data(company_type):
    files = ["ein", "duns", "ticker", "companies"]
    data = {}
    for file in files:
        folder = f"{DATA_PATH}/{file}"
        try:
            with open(
                f"{folder}/{company_type}.json",
                "r",
            ) as f:
                data[file] = json.load(f)
        except FileNotFoundError:
            print(f"File {file}_{company_type}.json not found.")
            data[file] = [{}] * len(
                data["companies"]
            )  # Empty dictionaries for missing data

    for index, company in enumerate(data["companies"]):
        for file in ["ein", "duns", "ticker"]:
            try:
                company.update(data[file][index])
            except IndexError:
                print(f"IndexError: {index}")
                continue

    try:
        with open(f"{DATA_PATH}/output/{company_type}.json", "w") as f:
            json.dump(data["companies"], f, indent=4)
    except FileNotFoundError:
        print(f"Could not write to {DATA_PATH}/output/{company_type}.json")

    convert_to_excel(
        f"{DATA_PATH}/output/{company_type}.json",
        f"{DATA_PATH}/update_companies.xlsx",
        company_type,
    )


def upload():
    """
    Parses command-line arguments and runs the appropriate functions based on those arguments.
    """
    parser = argparse.ArgumentParser(description="Run specific function.")
    add_arg(parser, "sponsor", "Update the spreadsheet with sponsor companies' data.")
    add_arg(parser, "exit", "Update the spreadsheet with exit-survey companies' data.")
    add_arg(parser, "visited", "Update the spreadsheet with visited companies' data.")

    args = parser.parse_args()
    if args.sponsor:
        merge_data("sponsor")
    elif args.exit:
        merge_data("exit")
    elif args.visited:
        merge_data("visited")


if __name__ == "__main__":
    upload()
