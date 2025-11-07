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
    """
    Read raw data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")

    # TODO: OPTIONAL Add data profiling here to understand the dataset
    # Suggestion: Log the datatypes of each column and the number of unique values
    # Example:
    # logger.info(f"Column datatypes: \n{df.dtypes}")
    # logger.info(f"Number of unique values: \n{df.nunique()}")

    return df


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
    df = df.dropna(subset=['productid'])  # Drop rows missing critical ID
    df['productid'] = df['productid'].fillna('Unknown')
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

    if 'unitprice' in df.columns:
        df = df[(df['unitprice'] > 200) & (df['unitprice'] < 800)]

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


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate data against business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Validated DataFrame.
    """
    logger.info(f"FUNCTION START: validate_data with dataframe shape={df.shape}")

    # TODO: Implement data validation rules specific to products
    # Suggestion: Check for valid values in critical fields
    # Example:
    # invalid_prices = df[df['price'] < 0].shape[0]
    # logger.info(f"Found {invalid_prices} products with negative prices")
    # df = df[df['price'] >= 0]

    logger.info("Data validation complete")
    return df


def main() -> None:
    """
    Main function for processing product data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_products_data.py")
    logger.info("==================================")

    logger.info(f"Root         : {PROJECT_ROOT}")
    logger.info(f"data/raw     : {RAW_DATA_DIR}")
    logger.info(f"data/prepared: {PREPARED_DATA_DIR}")
    logger.info(f"scripts      : {SCRIPTS_DIR}")

    input_file = "products_data.csv"
    output_file = "products_prepared.csv"

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

    # TODO:Remove outliers
    df = remove_outliers(df)

    # TODO: Validate data
    df = validate_data(df)

    # TODO: Standardize formats
    df = standardize_formats(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info(f"Original shape: {df.shape}")
    logger.info(f"Cleaned shape:  {original_shape}")
    logger.info("==================================")
    logger.info("FINISHED prepare_products_data.py")
    logger.info("==================================")


# -------------------
# Conditional Execution Block
# -------------------

if __name__ == "__main__":
    main()
