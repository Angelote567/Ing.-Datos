# Quick Data Check – E-Commerce Orders

## 1. How many rows do we have?
The dataset contains **189 rows** and **10 columns** (after skipping one malformed line).

## 2. Is there any sensitive information?
Yes, the file includes personal data such as:
- Customer names  
- Email addresses  
- Phone numbers  

## 3. What problems can this data have?
Several issues can appear:

- Missing values (Email, Phone, Price, Age)
- Invalid values (negative quantities, unrealistic ages, huge numbers)
- Inconsistent date formats
- Inconsistent country names
- Leading/trailing spaces in text fields
- Invalid email or phone formats  
- One malformed line in the CSV

These problems require cleaning before analysis.