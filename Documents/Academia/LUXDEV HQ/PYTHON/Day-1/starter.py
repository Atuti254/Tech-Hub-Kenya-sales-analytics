"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Prevents Tkinter GUI/DLL popup errors
import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        # Print the key and its data type, indented by spaces
        print(" " * indent + f"{key}: {type(value).__name__}")
        
        # If the value is itself a dictionary, call explore() on it recursively!
        if isinstance(value, dict):
            explore(value, indent + 2)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    flat_customers = []
    
    for c in customers:
        # Extract the email top-level domain (e.g., 'april.biz' -> 'biz')
        email_domain = c['email'].split('.')[-1]
        
        flat_record = {
            "customer_id": c['id'],
            "name": c['name'],
            "username": c['username'],
            "email": c['email'],
            "email_domain": email_domain,
            "phone": c['phone'],
            "city": c['address']['city'],
            "zipcode": c['address']['zipcode'],
            "latitude": float(c['address']['geo']['lat']),
            "longitude": float(c['address']['geo']['lng']),
            "company": c['company']['name'],
            "website": c['website']
        }
        flat_customers.append(flat_record)
        
    return flat_customers

def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c['city'] for c in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}
    for c in customers:
        city = c['city']
        counts[city] = counts.get(city, 0) + 1
    # Sort descending by count, then alphabetically by city
    sorted_counts = dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
    return sorted_counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = [c['email_domain'] for c in customers]
    counts = {domain: domains.count(domain) for domain in set(domains)}
    # Sort descending by count
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert flat customer records into a pandas DataFrame."""
    df = pd.DataFrame(rows)
    # Ensure correct column ordering matching expected output
    cols = [
        "customer_id", "name", "username", "email", "email_domain",
        "phone", "city", "zipcode", "latitude", "longitude", "company", "website"
    ]
    return df[cols]

def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(8, 5))
    plt.bar(counts.keys(), counts.values(), color='skyblue', edgecolor='black')
    plt.title("Customer Distribution by Email Domain")
    plt.xlabel("Email Top-Level Domain")
    plt.ylabel("Number of Customers")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

if __name__ == "__main__":
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # 1. Fetch data
    raw_customers = get_customers()
    print(f"Customers retrieved : {len(raw_customers)}")

    # 2. Explore first record
    if raw_customers:
        print("\n--- Record Structure ---")
        explore(raw_customers[0])

    # 3. Extract attributes
    flat_customers = extract_attributes(raw_customers)

    # 4. Unique cities
    cities = unique_cities(flat_customers)
    print(f"Unique cities       : {len(cities)}")

    # 5. Plain Python counts
    c_counts = city_counts(flat_customers)
    most_common_city = list(c_counts.keys())[0] if c_counts else "None"
    most_common_val = list(c_counts.values())[0] if c_counts else 0
    print(f"Most common city    : {most_common_city} ({most_common_val})")

    d_counts = email_domain_counts(flat_customers)
    print(f"Email domains       : {d_counts}")

    # 6. Convert to DataFrame
    df = to_dataframe(flat_customers)
    print(f"\nDataFrame shape: {df.shape}")
    print("\nDataFrame dtypes:\n", df.dtypes)

    # Verify counts with pandas
    print("\nPandas city counts:\n", df['city'].value_counts())

    # 7. Export CSVs
    df.to_csv(output_dir / "customers.csv", index=False)
    
    city_df = pd.DataFrame(list(c_counts.items()), columns=["city", "customer_count"])
    city_df.to_csv(output_dir / "city_counts.csv", index=False)

    # 8. Plot distribution (email domain distribution is more informative than city since each city has 1 customer)
    chart_path = output_dir / "customer_distribution.png"
    plot_distribution(d_counts, chart_path)
    print(f"Chart saved to      : {chart_path}")
