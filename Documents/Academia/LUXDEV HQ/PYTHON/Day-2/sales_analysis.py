"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics

Tasks 1-7 use only the standard library. pandas is allowed in task 8, to check your work.
"""
import csv
from pathlib import Path

DATA_PATH = Path("data") / "electronics_sales.csv"


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted."""
    if not value or not value.strip():
        return None
    cleaned = value.strip().replace(",", "").replace("KES", "").strip()
    try:
        val = float(cleaned)
        return val if val >= 0 else None  # Reject negative numbers if invalid
    except ValueError:
        return None


def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    clean_rows = []
    skipped_rows = []

    for raw_row in rows:
        row = {k.strip(): (v.strip() if v else "") for k, v in raw_row.items()}

        sale_id = row.get("sale_id", "UNKNOWN")
        qty = parse_number(row.get("quantity", ""))
        # Look for unit_price_kes first, fall back to unit_price if needed
        price_str = row.get("unit_price_kes") or row.get("unit_price", "")
        price = parse_number(price_str)

        if qty is None or price is None:
            reason = f"Invalid numeric value (qty='{row.get('quantity')}', price='{price_str}')"
            skipped_rows.append({"sale_id": sale_id, "reason": reason})
        else:
            clean_row = dict(row)
            clean_row["quantity"] = int(qty)
            clean_row["unit_price"] = price
            clean_row["revenue"] = clean_row["quantity"] * clean_row["unit_price"]
            clean_rows.append(clean_row)

    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    """Calculate the sum of all revenues from clean rows."""
    return sum(row["revenue"] for row in rows)


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals = {}
    for row in rows:
        key = row[field]
        if key in totals:
            totals[key] += row["revenue"]
        else:
            totals[key] = row["revenue"]
    return totals


def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    sorted_items = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return sorted_items[:n]


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    return [row for row in rows if row["revenue"] >= threshold]


# Reusable statistics - implement these yourself, no statistics module.
def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate median of empty list")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_vals[mid])
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    if not values:
        raise ValueError("Cannot calculate min/max of empty list")
    lowest = values[0]
    highest = values[0]
    for v in values[1:]:
        if v < lowest:
            lowest = v
        if v > highest:
            highest = v
    return lowest, highest


import pandas as pd

def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    # Read CSV
    df = pd.read_csv(path)

    # Apply cleaning logic to match standard library rules
    def clean_val(v):
        if pd.isna(v):
            return None
        cleaned = str(v).replace(",", "").replace("KES", "").strip()
        try:
            val = float(cleaned)
            return val if val >= 0 else None
        except ValueError:
            return None

    df["clean_qty"] = df["quantity"].apply(clean_val)
    price_col = "unit_price_kes" if "unit_price_kes" in df.columns else "unit_price"
    df["clean_price"] = df[price_col].apply(clean_val)

    clean_df = df.dropna(subset=["clean_qty", "clean_price"]).copy()
    clean_df["revenue"] = clean_df["clean_qty"] * clean_df["clean_price"]

    pd_total = clean_df["revenue"].sum()
    match_str = "MATCH" if abs(pd_total - my_results["total_revenue"]) < 1e-2 else "MISMATCH"
    print(f"Total revenue      : {match_str} (pure={my_results['total_revenue']:,.2f}, pandas={pd_total:,.2f})")


if __name__ == "__main__":
   # 1. Read raw CSV sales data
    raw_rows = read_sales(DATA_PATH)
    total_raw_rows = len(raw_rows)
    print("Total rows read:", total_raw_rows)
    if raw_rows:
        print("Sample raw row:", raw_rows[0])

    # 2. Convert and clean data
    clean_rows, skipped_rows = convert_rows(raw_rows)

    # 3. Compute total revenue
    tot_rev = total_revenue(clean_rows)

    # 4. Compute revenue breakdown by product
    prod_rev = revenue_by(clean_rows, "product")
    sorted_prod = sorted(prod_rev.items(), key=lambda x: x[1], reverse=True)

    # 5. Top 3 products
    top3 = top_n(prod_rev, 3)

    # 6. High-value sales (KES >= 50,000)
    hv_sales = high_value(clean_rows, 50000)

    # 7. Summary statistics for per-transaction revenue
    rev_list = [r["revenue"] for r in clean_rows]
    mean_val = mean(rev_list)
    med_val = median(rev_list)
    min_val, max_val = minimum_maximum(rev_list)

    # Build report text
    skipped_summary = ", ".join(f"{s['sale_id']}: {s['reason']}" for s in skipped_rows)

    report_lines = [
        "=== Sales report: September 2026 ===",
        f"Rows read          : {total_raw_rows}",
        f"Rows used          : {len(clean_rows)}",
        f"Rows skipped       : {len(skipped_rows)}   ({skipped_summary})",
        "",
        f"Total revenue (KES): {tot_rev:,.2f}",
        "",
        "Revenue by product (KES)",
    ]
    for p, amt in sorted_prod:
        report_lines.append(f"  {p:<20} {amt:,.2f}")

    report_lines.extend([
        "",
        "Top 3 products",
    ])
    for idx, (p, amt) in enumerate(top3, 1):
        report_lines.append(f"  {idx}. {p} - KES {amt:,.2f}")

    report_lines.extend([
        "",
        f"High-value transactions (>= KES 50,000): {len(hv_sales)}",
    ])
    for s in hv_sales:
        report_lines.append(
            f"  {s['sale_id']}  {s.get('date', '')}  {s['store']}  {s['product']}  KES {s['revenue']:,.2f}"
        )

    report_lines.extend([
        "",
        "Transaction revenue statistics",
        f"  mean   : {mean_val:,.2f}",
        f"  median : {med_val:,.2f}",
        f"  min    : {min_val:,.2f}",
        f"  max    : {max_val:,.2f}",
        ""
    ])

    full_report = "\n".join(report_lines)
    print(full_report)

    # Save output to output/sales_report.txt
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "sales_report.txt", "w", encoding="utf-8") as f:
        f.write(full_report + "\n")

    # 8. Run Pandas verification
    print("=== pandas verification ===")
    my_results = {
        "total_revenue": tot_rev,
        "product_revenue": prod_rev,
        "mean": mean_val,
        "median": med_val
    }
    verify_with_pandas(DATA_PATH, my_results)
