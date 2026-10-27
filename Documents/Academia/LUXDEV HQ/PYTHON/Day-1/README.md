# Pesa Pulse API Data Analysis

## Overview
Pesa Pulse, a Nairobi fintech start-up, recently partnered with an entity that provides access to its customer directory via a REST API. This project serves as an exploratory analysis of the customer dataset to answer foundational marketing questions: **How many customers are there? Where are they located? What does the data structure look like?**

The analysis retrieves nested JSON data, parses and flattens customer attributes using core Python structures, validates calculations using `pandas`, and exports structured CSVs alongside actionable data visualizations for marketing strategy.

---

## Technical Approach

### 1. Data Retrieval & Failure Handling
- **Endpoint**: `https://jsonplaceholder.typicode.com/users`
- **Tool**: `requests` library with a `timeout=5` setting.
- **Error Handling**: Uses `response.raise_for_status()` inside a `try...except` block catching `requests.exceptions.RequestException`. If a network failure occurs, it displays a clean error message without throwing a full traceback or crashing the pipeline.

### 2. Nested Structure Exploration
- **Recursive Inspection**: Implemented `explore(record, indent)` using `dict.items()` and `isinstance(value, dict)` to walk nested dictionaries recursively and print key names alongside their Python types indented by depth level.

### 3. Feature Extraction & Flattening
- **Extraction**: Mapped deeply nested JSON fields into flat dictionary structures.
- **Attributes Extracted**: `customer_id`, `name`, `username`, `email`, `email_domain`, `phone`, `city`, `zipcode`, `latitude`, `longitude`, `company`, and `website`.
- **Type Conversions**: `latitude` and `longitude` strings are safely converted to Python `float` values.
- **Parsing**: `email_domain` is extracted by taking the top-level domain suffix from the customer's email address (e.g., `Sincere@april.biz` -> `biz`).

### 4. Aggregation (Plain Python vs. Pandas)
- **Unique Cities**: Extracted distinct city names using a set comprehension (`{c['city'] for c in customers}`).
- **Frequency Counts**: Implemented custom dictionary iteration (`counts.get(city, 0) + 1`) and dictionary comprehensions without relying on `collections.Counter` or external libraries.
- **Validation**: Converted records into a `pandas.DataFrame` and cross-verified hand-written counts using `df['city'].value_counts()`.

### 5. Non-Interactive Visualization
- **Backend Setup**: Applied `matplotlib.use('Agg')` prior to loading Pyplot to ensure headless rendering and prevent system GUI/Tkinter window errors across execution environments.

---

## Key Findings & Marketing Insights

1. **Nested Data Hierarchy**:
   - The dataset contains nested dictionary objects under `address` and `company`. 
   - The deepest nested attributes are the geographic coordinates (`lat` and `lng`), located inside the `geo` dictionary under `address`.
   - **Access Path**: To access the deepest attribute: `record['address']['geo']['lat']`.

2. **Customer Geographical Distribution**:
   - **Total Customers**: 10
   - **Unique Cities**: 10
   - **Insight**: Every single customer in the API directory resides in a different city (1 customer per city). 
   - **Marketing Takeaway**: There is zero geographic clustering in this customer sample. Launching targeted regional or city-specific campaigns would yield low customer density per city.

3. **Email Top-Level Domain (TLD) Distribution**:
   - The most common email domain is `.biz` (3 out of 10 customers), while `.ca`, `.io`, `.org`, `.info`, `.tv`, `.me`, and `.net` account for 1 each.
   - **Chart Selection**: Charting customer distribution by **Email Domain** (`output/customer_distribution.png`) provides far more actionable insight for marketing segmentation than charting city distribution, as city counts are completely uniform (1 per city).

---

## Project Structure

```text
day1-api-analysis/
├── starter.py                 # Core analysis script implementing all tasks
├── requirements.txt           # Environment dependencies
├── README.md                  # Project documentation & findings
└── output/
    ├── customers.csv          # Exported flattened customer records
    ├── city_counts.csv        # Aggregated customer counts per city
    └── customer_distribution.png # Bar chart of email domain distribution