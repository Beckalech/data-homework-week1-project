import pathlib
import pandas as pd
import sys

# Add project root to sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# Local imports
from utils.data_scrubber import DataScrubber
from utils.logger import logger

# Define paths
CURRENT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
DATA_DIR = PROJECT_ROOT.parent / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"

CLEANED_DATA_DIR.mkdir(exist_ok=True)


def clean_and_save(file_name: str, cleaning_steps: list):
    input_path = RAW_DATA_DIR / file_name
    output_path = CLEANED_DATA_DIR / file_name.replace(".csv", "_cleaned.csv")

    logger.info(f"Loading {file_name}")
    df = pd.read_csv(input_path)
    original_shape = df.shape
    logger.info(f"Original shape: {original_shape}")

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    logger.info(f"Standardized column names: {list(df.columns)}")

    scrubber = DataScrubber(df)

    for step in cleaning_steps:
        before_shape = scrubber.df.shape
        scrubber.df = step(scrubber)
        after_shape = scrubber.df.shape
        logger.info(f"Applied {step.__name__}: shape changed from {before_shape} to {after_shape}")

    scrubber.df.to_csv(output_path, index=False)
    print(f"final dataframe shape: {scrubber.df.shape}")
    logger.info(f"Saved cleaned file to: {output_path}")


def main():
    logger.info("STARTING prepare_all_data.py")

    clean_and_save(
        "sales_data.csv",
        [
            lambda s: s.remove_duplicate_records(),
            lambda s: s.handle_missing_data(drop=True),
            lambda s: s.format_column_strings_to_upper_and_trim("customerid"),
            lambda s: s.filter_column_outliers("saleamount", 300, 1600),
            lambda s: s.parse_dates_to_add_standard_datetime("saledate"),
        ],
    )

    clean_and_save(
        "customers_data.csv",
        [
            lambda s: s.remove_duplicate_records(),
            lambda s: s.handle_missing_data(drop=True),
            lambda s: s.format_column_strings_to_upper_and_trim("customerid"),
            lambda s: s.format_column_strings_to_upper_and_trim("name"),
        ],
    )

    clean_and_save(
        "products_data.csv",
        [
            lambda s: s.remove_duplicate_records(),
            lambda s: s.handle_missing_data(drop=True),
            lambda s: s.format_column_strings_to_upper_and_trim("productid"),
            lambda s: s.format_column_strings_to_upper_and_trim("productname"),
        ],
    )

    logger.info("FINISHED prepare_all_data.py")


if __name__ == "__main__":
    main()
