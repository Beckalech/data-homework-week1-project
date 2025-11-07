#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Import from external packages (requires a virtual environment)
import pandas as pd

# Ensure project root is in sys.path for local imports (now 3 parents are needed)
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

# Import local modules (e.g. utils/logger.py)
from utils.logger import logger

# Optional: Use a data_scrubber module for common data cleaning tasks
from utils.data_scrubber import DataScrubber


# Constants
SCRIPTS_DATA_PREP_DIR: pathlib.Path = (
    pathlib.Path(__file__).resolve().parent
)  # Directory of the current script
SCRIPTS_DIR: pathlib.Path = SCRIPTS_DATA_PREP_DIR.parent
PROJECT_ROOT: pathlib.Path = SCRIPTS_DIR.parent
DATA_DIR: pathlib.Path = PROJECT_ROOT.parent / "data"
RAW_DATA_DIR: pathlib.Path = DATA_DIR / "raw"
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR / "prepared"  # place to store prepared data


# Ensure the directories exist or create them
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PREPARED_DATA_DIR.mkdir(exist_ok=True)

#####################################
# Define Functions - Reusable blocks of code / instructions
#####################################


def read_raw_data(file_name: str) -> pd.DataFrame:
    """Read raw data from CSV."""
    file_path: pathlib.Path = RAW_DATA_DIR.joinpath(file_name)
    try:
        logger.info(f"READING: {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if any other error occurs


def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of the output file.
    """
    logger.info(
        f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}"
    )
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.
    How do you decide if a row is duplicated?
    Which do you keep? Which do you delete?

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")

    # Let's delegate this to the DataScrubber class
    # First, create an instance of the DataScrubber class
    # by passing in the dataframe as an argument.
    df_scrubber = DataScrubber(df)

    # Now, call the method on our instance to remove duplicates.
    # This method will return a new dataframe with duplicates removed.
    df_deduped = df_scrubber.remove_duplicate_records()

    logger.info(f"Original dataframe shape: {df.shape}")
    logger.info(f"Deduped  dataframe shape: {df_deduped.shape}")
    return df_deduped


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values by filling or dropping.
    This logic is specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")

    # Log missing values count before handling
    missing_before = df.isna().sum().sum()
    logger.info(f"Total missing values before handling: {missing_before}")
    df = df.dropna(subset=['transactionid'])  # Drop rows missing critical ID
    df['transactionid'] = df['transactionid'].fillna('Unknown')
    # TODO: Fill or drop missing values based on business rules
    # Example:
    # df['CustomerName'].fillna('Unknown', inplace=True)
    # df.dropna(subset=['CustomerID'], inplace=True)

    # Log missing values count after handling
    missing_after = df.isna().sum().sum()
    logger.info(f"Total missing values after handling: {missing_after}")
    logger.info(f"{len(df)} records remaining after handling missing values.")
    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers based on thresholds.
    This logic is very specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    initial_count = len(df)

    if 'saleamount' in df.columns:
        df['saleamount'] = pd.to_numeric(df['saleamount'], errors='coerce')
        df = df.dropna(subset=['saleamount'])
        df = df[(df['saleamount'] > 300) & (df['saleamount'] < 1600)]

    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} outlier rows")
    logger.info(f"{len(df)} records remaining after removing outliers.")
    return df

    # TODO: Identify numeric columns that might have outliers.
    # Recommended - just use ranges based on reasonable data
    # People should not be 22 feet tall, etc.
    # OPTIONAL ADVANCED: Use IQR method to identify outliers in numeric columns
    # Example:
    # for col in ['price', 'weight', 'length', 'width', 'height']:
    #     if col in df.columns and df[col].dtype in ['int64', 'float64']:
    #         Q1 = df[col].quantile(0.25)
    #         Q3 = df[col].quantile(0.75)
    #         IQR = Q3 - Q1
    #         lower_bound = Q1 - 1.5 * IQR
    #         upper_bound = Q3 + 1.5 * IQR
    #         df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    #         logger.info(f"Applied outlier removal to {col}: bounds [{lower_bound}, {upper_bound}]")


def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the formatting of various columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with standardized formatting.
    """
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")

    # TODO: OPTIONAL ADVANCED Implement standardization for product data
    # Suggestion: Consider standardizing text fields, units, and categorical variables
    # Examples (update based on your column names and types):
    # df['product_name'] = df['product_name'].str.title()  # Title case for product names
    # df['category'] = df['category'].str.lower()  # Lowercase for categories
    # df['price'] = df['price'].round(2)  # Round prices to 2 decimal places
    # df['weight_unit'] = df['weight_unit'].str.upper()  # Uppercase units

    logger.info("Completed standardizing formats")
    return df


#####################################
# Define Main Function - The main entry point of the script
#####################################


def main() -> None:
    """
    Main function for processing data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_sales_data.py")
    logger.info("==================================")

    logger.info(f"Root         : {PROJECT_ROOT}")
    logger.info(f"data/raw     : {RAW_DATA_DIR}")
    logger.info(f"data/prepared: {PREPARED_DATA_DIR}")
    logger.info(f"scripts      : {SCRIPTS_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_prepared.csv"

    # Read raw data
    df = read_raw_data(input_file)

    # Record original shape
    original_shape = df.shape

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Log if any column names changed
    changed_columns = [
        f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new
    ]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Remove duplicates
    df = remove_duplicates(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Remove outliers
    df = remove_outliers(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {df.shape}")
    logger.info(f"Cleaned shape:  {original_shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_customers_data.py")
    logger.info("==================================")


#####################################
# Conditional Execution Block
# Ensures the script runs only when executed directly
# This is a common Python convention.
#####################################

if __name__ == "__main__":
    main()
