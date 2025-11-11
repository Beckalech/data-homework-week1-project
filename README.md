# Pro Analytics 02 Python Starter Repository

> Use this repo to start a professional Python project.

- Additional information: <https://github.com/denisecase/pro-analytics-02>
- Project organization: [STRUCTURE](./STRUCTURE.md)
- Build professional skills:
  - **Environment Management**: Every project in isolation
  - **Code Quality**: Automated checks for fewer bugs
  - **Documentation**: Use modern project documentation tools
  - **Testing**: Prove your code works
  - **Version Control**: Collaborate professionally

---

## WORKFLOW 1. Set Up Your Machine

Proper setup is critical.
Complete each step in the following guide and verify carefully.

- [SET UP MACHINE](./SET_UP_MACHINE.md)

---

## WORKFLOW 2. Set Up Your Project

After verifying your machine is set up, set up a new Python project by copying this template.
Complete each step in the following guide.

- [SET UP PROJECT](./SET_UP_PROJECT.md)

It includes the critical commands to set up your local environment (and activate it):

```shell
uv venv
uv python pin 3.12
uv sync --extra dev --extra docs --upgrade
uv run pre-commit install
uv run python --version
```

**Windows (PowerShell):**

```shell
.\.venv\Scripts\activate
```

**macOS / Linux / WSL:**

```shell
source .venv/bin/activate
```

---

## WORKFLOW 3. Daily Workflow

Please ensure that the prior steps have been verified before continuing.
When working on a project, we open just that project in VS Code.

### 3.1 Git Pull from GitHub

Always start with `git pull` to check for any changes made to the GitHub repo.

```shell
git pull
```

### 3.2 Run Checks as You Work

This mirrors real work where we typically:

1. Update dependencies (for security and compatibility).
2. Clean unused cached packages to free space.
3. Use `git add .` to stage all changes.
4. Run ruff and fix minor issues.
5. Update pre-commit periodically.
6. Run pre-commit quality checks on all code files (**twice if needed**, the first pass may fix things).
7. Run tests.

In VS Code, open your repository, then open a terminal (Terminal / New Terminal) and run the following commands one at a time to check the code.

```shell
uv sync --extra dev --extra docs --upgrade
uv cache clean
git add .
uvx ruff check --fix
uvx pre-commit autoupdate
uv run pre-commit run --all-files
git add .
uv run pytest
```

NOTE: The second `git add .` ensures any automatic fixes made by Ruff or pre-commit are included before testing or committing.

<details>
<summary>Click to see a note on best practices</summary>

`uvx` runs the latest version of a tool in an isolated cache, outside the virtual environment.
This keeps the project light and simple, but behavior can change when the tool updates.
For fully reproducible results, or when you need to use the local `.venv`, use `uv run` instead.

</details>

### 3.3 Build Project Documentation

Make sure you have current doc dependencies, then build your docs, fix any errors, and serve them locally to test.

```shell
uv run mkdocs build --strict
uv run mkdocs serve
```

- After running the serve command, the local URL of the docs will be provided. To open the site, press **CTRL and click** the provided link (at the same time) to view the documentation. On a Mac, use **CMD and click**.
- Press **CTRL c** (at the same time) to stop the hosting process.

### 3.4 Execute

This project includes demo code.
Run the demo Python modules to confirm everything is working.

In VS Code terminal, run:

```shell
uv run python -m analytics_project.demo_module_basics
uv run python -m analytics_project.demo_module_languages
uv run python -m analytics_project.demo_module_stats
uv run python -m analytics_project.demo_module_viz
```

You should see:

- Log messages in the terminal
- Greetings in several languages
- Simple statistics
- A chart window open (close the chart window to continue).

If this works, your project is ready! If not, check:

- Are you in the right folder? (All terminal commands are to be run from the root project folder.)
- Did you run the full `uv sync --extra dev --extra docs --upgrade` command?
- Are there any error messages? (ask for help with the exact error)

---

### 3.5 Git add-commit-push to GitHub

Anytime we make working changes to code is a good time to git add-commit-push to GitHub.

1. Stage your changes with git add.
2. Commit your changes with a useful message in quotes.
3. Push your work to GitHub.

```shell
git add .
git commit -m "describe your change in quotes"
git push -u origin main
```

This will trigger the GitHub Actions workflow and publish your documentation via GitHub Pages.

### 3.6 Modify and Debug

With a working version safe in GitHub, start making changes to the code.

Before starting a new session, remember to do a `git pull` and keep your tools updated.

Each time forward progress is made, remember to git add-commit-push.

### Smart Sales Project Setup

This section documents the setup steps I followed for the Smart Sales analytics project.

### Project Initialization
- Cloned the starter repository and created a local folder: `data-homework-week1-project`
- Opened the project folder in VS Code using **File > Open Folder**
- Verified presence of:
  - `README.md` in the root
  - `data/raw/` folder with CSV files
  - `.venv` virtual environment folder

### Added Starter Code
- Created a new file: `src/analytics_project/data_prep.py`
- Copied code from the [smart-sales-starter-files](https://github.com/denisecase/smart-sales-starter-files) GitHub repo
- Pasted code into 'src/analytic_project/data_prep.py'
- Saved the file in the correct folder

### Ran the Data Prep Module
- Opened the terminal in the root project folder
- Ran the module using:
  ```bash
  uv run python -m analytics_project.data_prep
- Checked the log file to make sure everything ran.
- Checked that one DataFrame populated for each raw data file.

### Pushed Changes to Git
- Used the following commands to push changes.
```shell
git add .
git commit -m "Add starter files"
git push -u origin main
```
- Updated ReadMe with changes and pushed to Git using the above commands with different commit comment.

## Project 3: Data Cleaning and Preparation

### Overview
This project implements a reusable data cleaning pipeline using a custom `DataScrubber` class to prepare three CSV files (sales, customers, and products) for ETL processing into a central data warehouse.

### File Structure
```
src/
├── utils/
│   └── data_scrubber.py          # Reusable DataScrubber class
└── analytics_project/
    └── data_preparation/
        └── prepare_all_data.py    # Data preparation pipeline script
data/
├── raw/                           # Original CSV files
│   ├── sales_data.csv
│   ├── customers_data.csv
│   └── products_data.csv
└── cleaned/                       # Cleaned output files
    ├── sales_data_cleaned.csv
    ├── customers_data_cleaned.csv
    └── products_data_cleaned.csv
```

### DataScrubber Class

The `DataScrubber` class (`src/utils/data_scrubber.py`) provides reusable methods for common data cleaning tasks:

**Key Methods:**
- `remove_duplicate_records()` - Removes duplicate rows from the DataFrame
- `handle_missing_data(drop=False, fill_value=None)` - Handles missing values by either dropping rows or filling with a specified value
- `format_column_strings_to_upper_and_trim(column)` - Converts string column to uppercase and removes whitespace
- `format_column_strings_to_lower_and_trim(column)` - Converts string column to lowercase and removes whitespace
- `filter_column_outliers(column, lower_bound, upper_bound)` - Filters rows based on numeric column thresholds
- `parse_dates_to_add_standard_datetime(column)` - Parses date strings and creates a standardized datetime column
- `rename_columns(column_mapping)` - Renames columns based on a mapping dictionary
- `reorder_columns(columns)` - Reorders DataFrame columns
- `drop_columns(columns)` - Removes specified columns
- `convert_column_to_new_data_type(column, new_type)` - Converts column data types
- `check_data_consistency_before_cleaning()` - Reports null counts and duplicate counts before cleaning
- `check_data_consistency_after_cleaning()` - Validates data after cleaning (asserts no nulls or duplicates)

### Data Preparation Pipeline

The `prepare_all_data.py` script applies the DataScrubber methods to all three data files with customized cleaning steps for each.

**Cleaning Steps Applied:**

#### Sales Data (`sales_data.csv`)
1. Remove duplicate records
2. Fill missing values with "N/A"
3. Convert customerid to uppercase and trim whitespace
4. Filter outliers: keep only sales between $300 and $1,600
5. Parse saledate and add StandardDateTime column

**Result:** 2,001 rows → 981 rows (1,020 rows removed by outlier filtering)

#### Customers Data (`customers_data.csv`)
1. Remove duplicate records
2. Fill missing values with "Unknown"
3. Convert customerid to uppercase and trim whitespace
4. Convert name to uppercase and trim whitespace

**Result:** 201 rows → 201 rows (no rows removed)

#### Products Data (`products_data.csv`)
1. Remove duplicate records
2. Fill missing values with "Unknown"
3. Convert productid to uppercase and trim whitespace
4. Convert productname to uppercase and trim whitespace

**Result:** 100 rows → 100 rows (no rows removed)

### Running the Data Preparation Script

**Command:**
```bash
python src/analytics_project/data_preparation/prepare_all_data.py
```

**Expected Output:**
```
2025-11-09 09:17:03,932 - INFO - STARTING prepare_all_data.py
2025-11-09 09:17:03,932 - INFO - Loading sales_data.csv
2025-11-09 09:17:03,936 - INFO - Original shape: (2001, 9)
2025-11-09 09:17:03,937 - INFO - Standardized column names: [...]
...
2025-11-09 09:17:03,947 - INFO - Saved cleaned file to: ...\data\cleaned\sales_data_cleaned.csv
...
2025-11-09 09:17:03,979 - INFO - FINISHED prepare_all_data.py
```

### Column Standardization

All column names are automatically standardized to:
- Lowercase
- Underscores instead of spaces
- Trimmed whitespace

**Example transformations:**
- `CustomerID` → `customerid`
- `Sale Date` → `sale_date`
- `Product Name` → `productname`

### Key Design Decisions

1. **Fill vs. Drop Missing Values:** Chose to fill missing values with meaningful placeholders ("N/A", "Unknown") rather than dropping rows to preserve maximum data for analysis.

2. **Outlier Filtering on Sales:** Applied aggressive outlier filtering (300-1600 range) on sales amounts to remove potentially erroneous transactions, reducing the dataset by ~50%.

3. **String Standardization:** Converted ID and name fields to uppercase for consistency across datasets, facilitating joins in future ETL processes.

4. **Datetime Parsing:** Added a standardized datetime column to sales data to enable time-based analysis and ensure consistent date formatting.

### Testing and Validation

The script includes logging at each step to track:
- Original data shape
- Shape changes after each cleaning operation
- Final output location
- Any errors encountered

Review the log output to verify cleaning operations performed as expected.

### Next Steps

The cleaned CSV files in `data/cleaned/` are now ready for:
- ETL processing into a central data warehouse
- Business intelligence queries
- Further analysis and visualization

### Issues Encountered and Resolved

1. **Column Name Mismatch:** Initial script referenced `customername` and incorrect column names. Fixed by checking actual standardized column names in log output and updating references to match (`name` for customers, `productname` for products).

2. **Code Formatting:** Resolved Ruff formatting issues by running `ruff format .` before committing.

### Git Workflow
```bash
# Format code
ruff format .

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Complete Project 3: Add data scrubber and cleaning pipeline"

# Push to GitHub
git push
```
"""
Creating a Data Warehouse

Project Overview
----------------
This project implements a data warehouse using a star schema design to support
business intelligence and analytics queries. The data warehouse consolidates
customer, product, and sales transaction data into a centralized repository
optimized for analytical workloads.

Schema Design
-------------
Design Choice: Star Schema
A star schema was selected for this data warehouse implementation due to its
simplicity and query performance benefits. The star schema consists of one
central fact table surrounded by dimension tables, minimizing the complexity
of joins and optimizing read operations for analytical queries.

Tables
------
Fact Table: sales
The sales table serves as the central fact table, containing quantitative
measures and foreign keys to dimension tables.

Columns:
- sale_id (INTEGER, PRIMARY KEY) : Unique identifier for each transaction
- date (TEXT) : Date of the transaction in ISO 8601 format (YYYY-MM-DD)
- customer_id (TEXT) : Foreign key reference to customers table
- product_id (TEXT) : Foreign key reference to products table
- store_id (TEXT) : Identifier for the store location
- campaign_id (TEXT) : Identifier for marketing campaign
- quantity (INTEGER) : Number of items purchased
- sales_amount (REAL) : Total sales amount for the transaction

Dimension Table: customers
The customers table contains descriptive attributes about customers.

Columns:
- customer_id (TEXT, PRIMARY KEY) : Unique identifier for each customer
- name (TEXT) : Customer name
- region (TEXT) : Geographic region where customer resides
- join_date (TEXT) : Date when customer joined in ISO 8601 format
- age (INTEGER) : Customer age
- gender (TEXT) : Customer gender

Dimension Table: products
The products table contains descriptive attributes about products.

Columns:
- product_id (TEXT, PRIMARY KEY) : Unique identifier for each product
- product_name (TEXT) : Name of the product
- category (TEXT) : Product category
- unit_price (REAL) : Price per unit of the product

Implementation Details
----------------------
Technology Stack:
- Database: SQLite
- Programming Language: Python 3.12
- Key Libraries:
  * pandas (data manipulation and loading)
  * sqlite3 (database connectivity)
  * pathlib (file path management)

ETL Process
-----------
The ETL (Extract, Transform, Load) process is implemented in
src/analytics_project/etl_to_dw.py and performs the following operations:

- Schema Creation: Creates the customers, products, and sales tables if they do not exist
- Data Extraction: Reads prepared CSV files from the data/prepared/ directory
- Data Transformation:
    * Renames columns from CSV format to match database schema conventions
      (lowercase with underscores)
    * Selects only relevant columns for each table
    * Ensures data types are compatible with the schema
- Data Loading: Inserts transformed data into the corresponding database tables
  using pandas .to_sql() method

File Structure
--------------
data-homework-week1-project/
├── data/
│   ├── prepared/
│   │   ├── customers_prepared.csv
│   │   ├── products_prepared.csv
│   │   └── sales_prepared.csv
│   └── dw/
│       └── my_datawarehouse.db
├── src/
│   └── analytics_project/
│       └── etl_to_dw.py
└── README.md

Data Naming Conventions
-----------------------
- Table names: Lowercase and pluralized (e.g., customers, products, sales)
- Column names: Lowercase with underscores separating words (e.g., customer_id, join_date)
- Date format: ISO 8601 format (YYYY-MM-DD) stored as TEXT for SQLite compatibility

Running the ETL Script
----------------------
To populate the data warehouse:

1. Ensure you are in the project root directory
2. Activate the virtual environment (if applicable)
3. Run the ETL script:

   python src/analytics_project/etl_to_dw.py

The script will output progress messages:
- Creating schema...
- Deleting existing records...
- Loading CSV files...
- Inserting customers...
- Inserting products...
- Inserting sales...
- Data warehouse loaded successfully!

Validation
----------
The data warehouse was validated using the SQLite Viewer extension in VS Code.
All three tables (customers, products, sales) were verified to contain the
correct data with proper relationships maintained through foreign keys.

Challenges Encountered
----------------------
- Foreign Key Syntax Error: Initial schema creation encountered syntax errors
  with FOREIGN KEY constraints in SQLite. Resolved by using executescript()
  method instead of execute() for multiple CREATE TABLE statements.
- Column Name Mismatch: CSV files used different naming conventions (CamelCase)
  than the database schema (lowercase with underscores). Resolved by
  implementing column renaming in the insert functions using pandas .rename().
- Duplicate Primary Key Error: Encountered UNIQUE constraint violations when
  re-running the script with existing data. Resolved by either deleting the
  database file or implementing DROP TABLE statements before schema creation.
- File Path Issues: Initial CSV import attempts in SQLite command line
  encountered file path resolution issues. Resolved by implementing Python-based
  ETL with pathlib for cross-platform file path management.
"""
