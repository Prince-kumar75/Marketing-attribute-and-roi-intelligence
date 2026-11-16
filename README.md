# Marketing Attribution and ROI Intelligence

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg)](https://powerbi.microsoft.com/)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL%20%7C%20MySQL%20%7C%20SQLite-336791.svg)](https://www.postgresql.org/)
[![Excel](https://img.shields.io/badge/Excel-Financial_Model-107C41.svg)](https://www.microsoft.com/excel)
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)]()

> An end-to-end Data Analyst & Business Intelligence project designed to analyze digital marketing campaign performance, calculate Return on Investment (ROI) and Return on Advertising Spend (ROAS), unpack customer journey touchpoints using Multi-Touch Attribution, and deliver actionable executive recommendations.

---

## 1. Project Overview & Business Problem

Modern enterprises deploy millions of dollars across fragmented digital channels (Google Ads, Facebook Ads, Instagram Ads, Email Marketing, Organic Search, Referral Marketing). However, marketing executives face two critical challenges:
1. **The Last-Touch Attribution Fallacy:** Traditional analytics tools credit 100% of conversion revenue to the last clicked link, causing brands to over-invest in closing channels (such as Brand Search and Email) while starving top-of-funnel discovery channels (such as Paid Social and Organic SEO).
2. **Capital Inefficiency:** Marketing budgets are frequently diluted by underperforming campaigns operating below break-even ROAS without detection.

### The Solution
This project follows a real-world Data Analyst workflow:
- **Data Ingestion & Cleaning:** Audits 8,572 campaign records and removes duplicates, repairs inconsistent formats, and handles outliers.
- **KPI Feature Engineering:** Formulates core business metrics (ROI, ROAS, CAC, CPC, CPL, CTR, Conversion Rate).
- **Multi-Touch Attribution Engine:** Models and compares First-Touch, Last-Touch, Linear, and Position-Based (40-40-20) attribution across 12,820 customer journey touchpoints.
- **SQL Analysis:** Executes 10+ business-oriented SQL queries utilizing CTEs, Window functions (`LAG`, `DENSE_RANK`, `FIRST_VALUE`, `LAST_VALUE`), and `CASE WHEN`.
- **Reporting & Dashboards:** Delivers an automated 5-tab Excel financial workbook, Power BI DAX schema, and an interactive 4-page HTML/JS executive dashboard.

---

## 2. Technology Stack

- **Data Processing & Analytics:** Python, Pandas, NumPy, SciPy
- **Data Visualization:** Matplotlib, Seaborn, Chart.js
- **Database & Querying:** SQL (PostgreSQL, MySQL, SQLite)
- **Business Intelligence & Reporting:** Power BI Desktop, Microsoft Excel (`openpyxl`), Jupyter Notebook (`.ipynb`)
- **Interactive UI:** HTML5, CSS3, JavaScript (ES6+), Chart.js

---

## 3. Repository Architecture

```text
Marketing attribute and roi intelligence/
├── README.md                                # Comprehensive project guide & documentation
├── requirements.txt                         # Python environment dependencies
│
├── data/
│   ├── raw/
│   │   └── marketing_campaign_data_raw.csv  # 8,620 raw records with real-world imperfections
│   └── processed/
│       ├── marketing_campaign_data_cleaned.csv       # 8,572 cleaned, validated records with KPIs
│       ├── customer_attribution_touchpoints.csv      # 12,820 customer multi-touch events
│       ├── customer_attribution_modeled.csv          # Journey-level attribution weights
│       ├── marketing_attribution_summary.csv         # Channel revenue by attribution model
│       └── monthly_channel_summary.csv               # Monthly channel aggregations
│
├── notebooks/
│   └── marketing_attribution_roi_analysis.ipynb      # Fully executed Jupyter Notebook with embedded plots
│
├── sql/
│   ├── create_tables.sql                    # PostgreSQL / MySQL DDL schema and indexes
│   └── marketing_analytics_queries.sql      # 10 business queries + attribution SQL CTEs
│
├── src/
│   ├── __init__.py                          # Package initialization
│   ├── data_generator.py                    # Synthetic dataset generation engine
│   ├── data_cleaning.py                     # Data cleaning & feature engineering pipeline
│   ├── attribution.py                       # Multi-touch attribution mathematical engine
│   ├── eda.py                               # Exploratory data analysis & figure generator
│   └── excel_generator.py                   # 5-tab executive Excel report generator
│
├── power_bi/
│   ├── README_powerbi.md                    # Step-by-step Power BI setup & visual guide
│   ├── dax_measures.dax                     # 35+ enterprise DAX formulas
│   └── data_model_schema.json               # Star schema data model definition
│
├── dashboard/
│   ├── index.html                           # 4-page standalone interactive dashboard
│   ├── styles.css                           # Executive responsive styling
│   ├── app.js                               # Dashboard controller & Chart.js driver
│   └── dashboard_data.js                    # Embedded dataset for zero-CORS browser execution
│
├── reports/
│   ├── business_intelligence_report.md      # C-Suite executive briefing & strategic roadmap
│   ├── marketing_roi_intelligence_report.xlsx # 5-tab formatted Excel financial report
│   ├── sql_query_results.md                 # Verified markdown output tables of all SQL queries
│   └── figures/                             # 8 publication-quality figures
│       ├── 01_channel_spend_vs_revenue.png
│       ├── 02_channel_roi_roas_comparison.png
│       ├── 03_monthly_revenue_and_spend_trends.png
│       ├── 04_attribution_model_comparison.png
│       ├── 05_cac_and_cpc_by_channel.png
│       ├── 06_conversion_funnel_rates.png
│       ├── 07_campaign_profitability_matrix.png
│       └── 08_channel_revenue_share_pie.png
│
└── scripts/
    ├── generate_all.py                      # Master pipeline orchestrator
    ├── run_sql_analysis.py                  # SQL query runner & verifier
    ├── export_dashboard_data.py             # Dashboard JSON/JS data exporter
    └── build_notebook.py                    # In-process notebook generator & executor
```

---

## 4. Key Performance Indicators (KPIs) Formulations

| Metric | Formula | Business Interpretation |
| :--- | :--- | :--- |
| **Net Profit** | $\text{Revenue} - \text{Spend}$ | True dollar contribution margin generated by marketing. |
| **ROI (%)** | $\frac{\text{Revenue} - \text{Spend}}{\text{Spend}} \times 100$ | Capital return efficiency per dollar spent. |
| **ROAS** | $\frac{\text{Revenue}}{\text{Spend}}$ | Revenue multiple generated per advertising dollar. |
| **CAC** | $\frac{\text{Marketing Spend}}{\text{Conversions}}$ | Average acquisition cost to acquire one paying customer. |
| **Conversion Rate (%)** | $\frac{\text{Conversions}}{\text{Clicks}} \times 100$ | Percentage of website visitors who complete a transaction. |
| **CPC** | $\frac{\text{Marketing Spend}}{\text{Clicks}}$ | Unit cost per visitor traffic acquired. |
| **CPL** | $\frac{\text{Marketing Spend}}{\text{Leads}}$ | Cost per inbound qualified lead generated. |
| **CTR (%)** | $\frac{\text{Clicks}}{\text{Impressions}} \times 100$ | Ad creative engagement and clickability. |

---

## 5. Executive Macro Findings (FY 2025 Audit)

```
========================================================================
             FY 2025 PORTFOLIO FINANCIAL AUDIT SUMMARY
========================================================================
 Total Marketing Capital Deployed:      $4,678,276.51
 Total Gross Revenue Generated:         $52,091,563.43
 Net Marketing Contribution Profit:     $47,413,286.92
 Overall Portfolio ROAS Multiple:       11.13x
 Blended Portfolio ROI (%):             1,013.48%
 Total Customer Conversions:            311,114
 Total Qualified Inbound Leads:         869,457
 Blended Customer Acquisition Cost:     $15.04
 Blended Cost Per Click (CPC):          $0.87
 Overall Funnel Conversion Rate:        5.76%
========================================================================
```

### Channel Performance Breakdown

| Marketing Channel | Total Spend (\$) | Total Revenue (\$) | Net Profit (\$) | ROAS | ROI (%) | CAC (\$) | Conv. Rate (%) | Role in Portfolio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Organic Search** | \$422,825.41 | \$20,858,828.91 | \$20,436,003.50 | **49.33x** | 4,833.2% | \$3.38 | 6.22% | Foundation & First-Touch Driver |
| **Email Marketing** | \$268,273.40 | \$12,105,908.49 | \$11,837,635.09 | **45.13x** | 4,412.5% | \$3.65 | 8.54% | High-Converting Owned Channel |
| **Referral Marketing** | \$582,772.19 | \$8,295,055.41 | \$7,712,283.22 | **14.23x** | 1,323.4% | \$12.58 | 6.98% | High-Trust Word of Mouth |
| **Google Ads** | \$1,397,654.59 | \$4,761,599.72 | \$3,363,945.13 | **3.41x** | 240.7% | \$46.83 | 5.48% | Intent Capture & Closing Driver |
| **Facebook Ads** | \$1,099,135.87 | \$3,620,927.28 | \$2,521,791.41 | **3.29x** | 229.4% | \$50.43 | 3.52% | Top-of-Funnel Prospecting |
| **Instagram Ads** | \$907,615.05 | \$2,449,243.62 | \$1,541,628.57 | **2.70x** | 169.9% | \$62.53 | 2.81% | Visual Brand Discovery |

---

## 6. Multi-Touch Attribution Insights

In digital marketing, customer paths are rarely single-touch. Across 5,500 customer journeys analyzed:
- 70% of converting customers interacted with 2 to 5 touchpoints across multiple channels.
- Comparing single-touch vs. multi-touch models reveals significant channel bias:

| Marketing Channel | First-Touch Share | Last-Touch Share | Position-Based (40-40-20) | Attribution Shift (Last - First) | Strategic Reality |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Google Ads** | 9.94% | **34.02%** | **21.17%** | **+\$133,715.81** | *Closer:* Captures existing demand before purchase. |
| **Organic Search** | **36.11%** | 18.92% | **26.61%** | **-\$95,466.48** | *Opener:* Discovers brands via informative content. |
| **Facebook Ads** | **28.19%** | 12.62% | **20.17%** | **-\$86,459.80** | *Opener:* Creates interest and initiates buyer journeys. |
| **Instagram Ads** | 20.66% | 10.31% | **15.63%** | **-\$57,460.98** | *Opener:* Visual discovery and consideration. |
| **Email Marketing** | 2.80% | **15.40%** | **9.80%** | **+\$69,957.76** | *Nurturer/Closer:* Re-engages cart abandoners. |
| **Referral Marketing**| 2.30% | 8.73% | 6.62% | **+\$35,713.69** | *Closer:* Validates social proof at checkout. |

> **Critical Takeaway:** Relying solely on Last-Touch attribution creates a false impression that Facebook and Instagram are failing. Cutting their budget would eliminate 48.85% of initial customer interactions, causing downstream Google Search conversions to collapse. **Position-Based Attribution (40-40-20)** provides the most accurate view for marketing budget allocation.

---

## 7. SQL Analysis Overview

The file [`sql/marketing_analytics_queries.sql`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/sql/marketing_analytics_queries.sql) covers all 10 core business requirements plus advanced attribution CTEs:

1. **Query 1:** Macro portfolio expenditure, revenue, profit, and blended ROI.
2. **Query 2:** Channel revenue, spend, and ROAS with window percentage shares.
3. **Query 3:** Top 5 profitable campaigns by net dollar contribution.
4. **Query 4:** Performance tier categorization using `CASE WHEN` (Elite, Strong, Moderate, Loss-Making).
5. **Query 5:** Funnel conversion velocity (CTR, Lead Rate, Conversion Rate) by channel.
6. **Query 6:** Anomaly detection: High spend, low ROAS campaigns using CTEs and `HAVING`.
7. **Query 7:** Month-over-Month (MoM) revenue momentum utilizing `LAG() OVER (ORDER BY year, month)`.
8. **Query 8:** Composite channel effectiveness ranking (ROAS, CAC, and Conv Rate ranks).
9. **Query 9:** CAC audit across channels and operational campaign statuses (`Active`, `Completed`, `Paused`).
10. **Query 10:** Global campaign leaderboard using `DENSE_RANK() OVER (ORDER BY roas DESC)`.
11. **Query 11 (Bonus):** Pure SQL Multi-Touch Attribution comparison using `FIRST_VALUE()` and `LAST_VALUE()` with window frames.

*To review the complete output tables, inspect [`reports/sql_query_results.md`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/reports/sql_query_results.md).*

---

## 8. Power BI Dashboard Specifications

The Power BI implementation contains 4 dedicated report pages designed for executive decision-making:

- **Global Slicers:** Date Range, Marketing Channel, Campaign Status, Campaign Name Search.
- **Page 1: Executive Overview:**
  - 6 KPI Scorecards: Spend, Revenue, ROI %, ROAS, Conversions, Leads.
  - Combo bar/line chart of monthly revenue vs. spend momentum.
  - Donut chart of revenue share by channel.
  - Executive performance matrix with conditional formatting.
- **Page 2: Channel Performance:**
  - Channel ROI and ROAS side-by-side bar charts.
  - Efficiency scatter matrix (CAC vs. ROAS vs. Conversions).
  - Funnel velocity drop-off chart.
- **Page 3: Campaign Analysis:**
  - Top 10 Star Campaigns by Net Profit.
  - Bottom 10 Budget Bleeder Campaigns by ROAS.
  - Decomposition tree (Revenue by Channel -> Status -> Campaign).
- **Page 4: Attribution Analysis:**
  - Clustered column chart comparing revenue under First-Touch, Last-Touch, Linear, and Position-Based models.
  - Waterfall chart displaying attribution shift (Last-Touch minus First-Touch).

*See [`power_bi/README_powerbi.md`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/power_bi/README_powerbi.md) for detailed DAX measures and model instructions.*

---

## 9. Interactive Browser Dashboard

In addition to Power BI, an interactive dashboard is available in the [`dashboard/`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/dashboard/) directory. It runs locally in any web browser without needing a web server or database setup.

To open the dashboard:
1. Double-click [`dashboard/index.html`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/dashboard/index.html) in your browser.
2. Toggle between the 4 pages using the sidebar.
3. Filter by Marketing Channel or Campaign Status using the top slicer bar.
4. Hover over charts to view interactive tooltips.

---

## 10. How to Run & Reproduce the Project

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Virtual environment (recommended)

### Installation
```bash
# Clone or navigate to the workspace
cd "Marketing attribute and roi intelligence"

# Install required Python dependencies
pip install -r requirements.txt
```

### End-to-End Pipeline Execution
Run the master pipeline script to regenerate all cleaned datasets, run attribution models, generate figures, run SQL queries, compile the Excel report, update dashboard data, and build the Jupyter notebook:

```bash
python scripts/generate_all.py
```

### Individual Execution Modules
```bash
# Run data cleaning & feature engineering
python src/data_cleaning.py

# Run multi-touch attribution engine
python src/attribution.py

# Run EDA and generate all report figures
python src/eda.py

# Generate executive Excel report (.xlsx)
python src/excel_generator.py

# Execute and verify SQL queries
python scripts/run_sql_analysis.py

# Build and execute Jupyter Notebook (.ipynb)
python scripts/build_notebook.py
```

---

## 11. Key Deliverables Summary

1. **Cleaned Marketing Dataset:** [`data/processed/marketing_campaign_data_cleaned.csv`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/data/processed/marketing_campaign_data_cleaned.csv)
2. **Customer Attribution Touchpoints:** [`data/processed/customer_attribution_touchpoints.csv`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/data/processed/customer_attribution_touchpoints.csv)
3. **Attribution Summary:** [`data/processed/marketing_attribution_summary.csv`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/data/processed/marketing_attribution_summary.csv)
4. **Python Jupyter Notebook:** [`notebooks/marketing_attribution_roi_analysis.ipynb`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/notebooks/marketing_attribution_roi_analysis.ipynb)
5. **SQL Analytical Queries:** [`sql/marketing_analytics_queries.sql`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/sql/marketing_analytics_queries.sql) & Results: [`reports/sql_query_results.md`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/reports/sql_query_results.md)
6. **Excel Financial Report:** [`reports/marketing_roi_intelligence_report.xlsx`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/reports/marketing_roi_intelligence_report.xlsx)
7. **Power BI Deliverables:** [`power_bi/README_powerbi.md`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/power_bi/README_powerbi.md) & [`power_bi/dax_measures.dax`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/power_bi/dax_measures.dax)
8. **Interactive Web Dashboard:** [`dashboard/index.html`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/dashboard/index.html)
9. **Executive Business Report:** [`reports/business_intelligence_report.md`](file:///c:/Users/princ/OneDrive/Desktop/Marketing%20attribute%20and%20roi%20intelligence/reports/business_intelligence_report.md)
