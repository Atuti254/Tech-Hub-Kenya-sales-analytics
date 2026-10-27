# Tech Hub Kenya — September 2026 Sales Analytics

## Overview

This project delivers an automated sales analysis script for Tech Hub Kenya. As part of the Day 2 Data Science curriculum, the primary objective is to process raw sales data across retail branches in Nairobi, Mombasa, Kisumu, and Nakuru to compute core financial metrics: total revenue, product performance breakdowns, high-value transaction identification, and descriptive statistics.

### Environment Constraints

To meet production deployment constraints where the reporting server lacks external package installations, all data parsing, cleaning, aggregation, and statistics are implemented strictly using Python's standard library. Pandas is restricted to an automated post-verification function (`verify_with_pandas`) to validate the accuracy of the standard library implementation.

---

## Project Structure

```text
day2-sales-analytics/
├── sales_analysis.py       # Main Python script containing all standard library & verification logic
├── data/
│   └── electronics_sales.csv  # Input till export dataset
├── output/
│   └── sales_report.txt    # Generated text report
├── requirements.txt        # Package dependencies (pandas for verification)
└── README.md               # Project documentation