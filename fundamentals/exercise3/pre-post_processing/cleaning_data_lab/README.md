# Quick Data Check – E-Commerce Orders (Raw & Cleaned)

## 1. How many rows do we have?
The raw dataset contains **189 rows** and **10 columns**  
(after skipping one malformed line detected by Pandas).

The cleaned dataset also contains **189 rows**  
(no rows were removed, but many values were corrected).

## 2. Is there any sensitive information?
Yes — the dataset contains personal information:

- Customer names  
- Email addresses  
- Phone numbers  
- Country of residence  
- Order details tied to individuals  

This means the dataset must be handled with care.

## 3. What problems can this data have?
The raw file showed multiple data-quality issues:

### **Missing / incomplete data**
- Emails missing
- Phone numbers missing
- Prices and ages missing
- Dates that cannot be parsed → become `NaT`

### **Invalid or unrealistic values**
- Quantities of **0**, negative, or extreme values (e.g., 40,000)
- Ages like **-5**, **999**, or **"unknown"**
- Prices missing or incorrectly typed

### **Inconsistent formatting**
- Mixed date formats  
  (e.g., `2023-01-15`, `03/01/2023`, `2023/03/14`)
- Country names not standardized  
  (`usa`, `US`, `united states`, `Gb`, etc.)
- Text fields with leading/trailing spaces
- Inconsistent phone formatting

### **Malformed input**
- One row in the CSV contains **11 fields instead of 10**,  
  causing Pandas to warn and skip it.

### **Email / phone structure problems**
- Values like `"invalid_email"`  
- Phones with spaces, text, or missing values

### **Duplicates**
- No duplicated full rows  
- No duplicated OrderIDs  
  (Uniqueness: OK)

---

## 4. What have we done in the cleaning process?
The script performs a complete automated cleaning pipeline:

- Removed fully duplicated rows  
- Trimmed whitespace in text fields  
- Standardized country names (`usa`, `us` → `USA`, etc.)
- Converted:
  - Dates to `datetime`
  - Quantity, Price, CustomerAge to numeric
- Replaced `"unknown"` and invalid ages with `NaN`
- Marked impossible values (negative, `>120`, `>1000`) as invalid
- Filled missing numeric values with the median
- Left invalid dates as `NaT` for transparency
- Exported the cleaned file: **cleaned_ecommerce_orders.csv**

---

## 5. Data quality tests performed
We calculated 5 data-quality dimensions for **raw** and **cleaned** data:

- **Accuracy**  
  Valid numeric values: positive quantities, realistic ages, valid prices.

- **Completeness**  
  Required fields: Email, Price, CustomerAge.

- **Consistency**  
  Country format matches accepted values.

- **Validity**  
  Email contains `@` and `.`, date parses correctly, numeric values valid.

- **Uniqueness**  
  No duplicated OrderIDs.

These scores show how much the dataset improved after cleaning.

---

The final script retrieves the data, analyzes it, cleans it, evaluates data quality, and exports a clean version ready for analysis.
