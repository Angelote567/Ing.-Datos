"""
DATA CLEANING EXERCISE
=====================
Retrieve, explore, and clean an e-commerce customer orders dataset
"""
import os
import requests
from datetime import datetime
import pandas as pd
import io

print("=" * 70)
print("DATA CLEANING EXERCISE - E-COMMERCE CUSTOMER ORDERS")
print("=" * 70)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: RETRIEVE DATA FROM WEB SOURCE
# ============================================================================
print("STEP 1: RETRIEVING DATA FROM WEB SOURCE")
print("-" * 70)

url = "https://raw.githubusercontent.com/victorbrub/data-engineering-class/refs/heads/main/pre-post_processing/exercise.csv"

try:
    print(f"Fetching data from: {url}")
    response = requests.get(url, timeout=10)

    print("Response:", response.text)

    print("Data fetched from web source, loading into DataFrame...")
    df = pd.read_csv(io.StringIO(response.text), sep=",", on_bad_lines="warn")

    print(f"Data retrieved successfully!")
    print(f"Status Code: {response.status_code}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}\n")
    print(df.head())

except Exception as e:
    print(f"✗ Error: {e}")
    raise e

# Keep a copy of the RAW data (before cleaning) for quality tests
raw_df = df.copy(deep=True)

# ============================================================================
# STEP 2: INITIAL EXPLORATION
# ============================================================================
print("STEP 2: INITIAL DATA EXPLORATION")
print("-" * 70)
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn Names & Types:\n{df.dtypes}")
print(f"\nFirst 5 Rows:\n{df.head()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nTotal Missing: {df.isnull().sum().sum()}\n")

# ============================================================================
# STEP 3: IDENTIFY QUALITY ISSUES
# ============================================================================
print("STEP 3: DATA QUALITY ISSUES")
print("-" * 70)

print(f"Duplicates: {df.duplicated().sum()}")
print(f"Duplicate OrderIDs: {df['OrderID'].duplicated().sum()}")

if df[df.duplicated(subset=["OrderID"], keep=False)].shape[0] > 0:
    print(
        f"\nDuplicate Records:\n"
        f"{df[df.duplicated(subset=['OrderID'], keep=False)].sort_values('OrderID')}\n"
    )

# ============================================================================
# STEP 4: DATA CLEANING
# ============================================================================
print("STEP 4: DATA CLEANING")
print("-" * 70)

# Save number of rows and missing values before cleaning (for the summary)
initial_rows = len(df)
missing_before = df.isnull().sum().sum()

# 4.1 Remove fully duplicated rows
df = df.drop_duplicates()
print(f"✓ Removed duplicate rows: {initial_rows - len(df)}")

# 4.2 Normalize column names (in case they come with spaces)
df.columns = df.columns.str.strip()

# 4.3 Trim whitespace in text columns
text_cols = ["CustomerName", "Email", "Phone", "Country", "OrderStatus"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# 4.4 Convert data types
# OrderDate → datetime (accept multiple formats)
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

# Quantity and Price → numeric
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# CustomerAge has "unknown", negative values and 999 → handle them
df["CustomerAge"] = df["CustomerAge"].replace("unknown", pd.NA)
df["CustomerAge"] = pd.to_numeric(df["CustomerAge"], errors="coerce")

# 4.5 Simple rules for impossible values / outliers
# Quantities <= 0 or extremely large are marked as NA
df.loc[df["Quantity"] <= 0, "Quantity"] = pd.NA
df.loc[df["Quantity"] > 1000, "Quantity"] = pd.NA  # 40000, etc.

# Negative ages or >120 are also considered invalid
df.loc[df["CustomerAge"] <= 0, "CustomerAge"] = pd.NA
df.loc[df["CustomerAge"] > 120, "CustomerAge"] = pd.NA  # 999, 150, etc.

# 4.6 Standardize country names
country_map = {
    "usa": "USA",
    "us": "USA",
    "united states": "USA",
    "united kingdom": "UK",
    "uk": "UK",
    "gb": "UK",
    "canada": "CANADA",
}
df["Country"] = (
    df["Country"]
    .str.strip()
    .str.lower()
    .map(country_map)
    .fillna(df["Country"].str.strip().str.upper())
)

# 4.7 Fill missing values in numeric columns with the median
qty_median = df["Quantity"].median()
price_median = df["Price"].median()
age_median = df["CustomerAge"].median()

df["Quantity"] = df["Quantity"].fillna(qty_median)
df["Price"] = df["Price"].fillna(price_median)
df["CustomerAge"] = df["CustomerAge"].fillna(age_median)

missing_after = df.isnull().sum().sum()

print(f"✓ Missing values before: {missing_before}, after: {missing_after}")
print("✓ Data cleaning finished\n")

# ============================================================================
# STEP 5: FINAL VALIDATION
# ============================================================================
print("STEP 5: FINAL VALIDATION")
print("-" * 70)

print(f"Final Shape: {df.shape}")
print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nData Types After Cleaning:")
print(df.dtypes)

print("\nSample Clean Data:")
print(df.head())

# ============================================================================
# STEP 6: SAVE CLEANED DATA
# ============================================================================
print("STEP 6: SAVING CLEANED DATA")
print("-" * 70)

output_path = "cleaned_ecommerce_orders.csv"
df.to_csv(output_path, index=False)

print(f"✓ Cleaned dataset saved as: {output_path}\n")

# ============================================================================
# STEP 7: DATA QUALITY TESTS (RAW VS CLEANED)
# ============================================================================
print("STEP 7: DATA QUALITY TESTS (RAW VS CLEANED)")
print("-" * 70)


def compute_quality_scores(df_in: pd.DataFrame, name: str):
    """Compute simple data quality metrics for the given DataFrame."""
    n = len(df_in)
    print(f"\nData quality scores for: {name}")
    print(f"Total rows: {n}")

    # --- Accuracy ---
    qty = pd.to_numeric(df_in["Quantity"], errors="coerce")
    price = pd.to_numeric(df_in["Price"], errors="coerce")
    age = (
        df_in["CustomerAge"]
        .replace("unknown", pd.NA)
        .pipe(pd.to_numeric, errors="coerce")
    )
    mask_accuracy = (
        qty.notna()
        & price.notna()
        & age.notna()
        & (qty > 0)
        & (qty <= 1000)
        & (price > 0)
        & (age > 0)
        & (age <= 120)
    )
    accuracy = mask_accuracy.mean()

    # --- Completeness ---
    required_cols = ["Email", "Price", "CustomerAge"]
    mask_completeness = df_in[required_cols].notna().all(axis=1)
    completeness = mask_completeness.mean()

    # --- Consistency (countries) ---
    country = df_in["Country"].astype(str).str.strip()
    lower_country = country.str.lower()
    allowed_raw = [
        "usa",
        "us",
        "united states",
        "united kingdom",
        "uk",
        "gb",
        "canada",
    ]
    mask_consistency = lower_country.isin(allowed_raw)
    consistency = mask_consistency.mean()

    # --- Validity (email + numeric + date) ---
    email = df_in["Email"].astype(str).str.strip()
    mask_email_valid = (
        email.str.contains("@")
        & email.str.contains(r"\.", regex=True)
        & ~email.str.contains("invalid_email", case=False)
    )
    date_parsed = pd.to_datetime(df_in["OrderDate"], errors="coerce")
    mask_valid = (
        mask_email_valid
        & date_parsed.notna()
        & qty.notna()
        & price.notna()
    )
    validity = mask_valid.mean()

    # --- Uniqueness (OrderID) ---
    mask_unique = ~df_in["OrderID"].duplicated(keep=False)
    uniqueness = mask_unique.mean()

    # Print scores as percentages
    print(f"Accuracy:     {accuracy:6.2%}")
    print(f"Completeness: {completeness:6.2%}")
    print(f"Consistency:  {consistency:6.2%}")
    print(f"Validity:     {validity:6.2%}")
    print(f"Uniqueness:   {uniqueness:6.2%}")


# Compare RAW vs CLEANED
compute_quality_scores(raw_df, "RAW DATA")
compute_quality_scores(df, "CLEANED DATA")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "-" * 70)
print(f"Initial rows: {initial_rows}")
print(f"Final rows:   {len(df)}")
print(f"Duplicates removed: {initial_rows - len(df)}")
print(f"Missing values remaining: {df.isnull().sum().sum()}")
print(f"Dataset saved to: {output_path}")
print("-" * 70)

print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
