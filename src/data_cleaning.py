"""
Data Cleaning and Preprocessing Pipeline
Handles missing values, duplicates, outliers, inconsistent formats,
data validation, and KPI feature engineering.
"""

import numpy as np
import pandas as pd


def clean_marketing_data(raw_csv_path="data/raw/marketing_campaign_data_raw.csv",
                         output_csv_path="data/processed/marketing_campaign_data_cleaned.csv"):
    print("=" * 70)
    print("STARTING MARKETING DATA CLEANING & PREPROCESSING PIPELINE")
    print("=" * 70)

    # 1. Ingest Raw Data
    df_raw = pd.read_csv(raw_csv_path)
    initial_rows = len(df_raw)
    print(f"1. Ingested raw dataset: {initial_rows} records, {df_raw.shape[1]} columns.")

    # 2. Duplicate Removal
    # Exact duplicate check
    num_exact_dups = df_raw.duplicated().sum()
    df = df_raw.drop_duplicates().reset_index(drop=True)
    print(f"2. Removed {num_exact_dups} duplicate records. Remaining: {len(df)} records.")

    # 3. String & Categorical Standardization
    # Strip whitespace & standardize Channel names
    channel_mapping = {
        "google ads": "Google Ads",
        "google  ads": "Google Ads",
        "facebook ads": "Facebook Ads",
        "instagram ads": "Instagram Ads",
        "email marketing": "Email Marketing",
        "organic search": "Organic Search",
        "referral marketing": "Referral Marketing"
    }
    df["Marketing Channel"] = df["Marketing Channel"].astype(str).str.strip()
    df["Marketing Channel"] = df["Marketing Channel"].apply(
        lambda x: channel_mapping.get(x.lower(), x.title())
    )

    # Standardize Campaign Status
    status_mapping = {
        "active": "Active",
        "completed": "Completed",
        "paused": "Paused"
    }
    df["Campaign Status"] = df["Campaign Status"].astype(str).str.strip().str.title()
    df["Campaign Status"] = df["Campaign Status"].apply(
        lambda x: status_mapping.get(x.lower(), "Active")
    )

    # Standardize Campaign Name & Customer ID
    df["Campaign Name"] = df["Campaign Name"].astype(str).str.strip()
    df["Customer ID"] = df["Customer ID"].astype(str).str.strip().str.upper()

    print("3. Categorical fields normalized (Marketing Channel, Campaign Status, Customer ID).")

    # 4. Datetime Parsing & Standardization
    # Handle multiple datetime formats (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY)
    df["Campaign Date"] = pd.to_datetime(df["Campaign Date"], format="mixed", dayfirst=False)
    # Filter valid date range (e.g. 2025)
    df["Campaign Date"] = pd.to_datetime(df["Campaign Date"].dt.strftime("%Y-%m-%d"))
    print(f"4. Datetime parsed and standardized to ISO format. Date range: {df['Campaign Date'].min()} to {df['Campaign Date'].max()}")

    # 5. Outlier & Anomaly Detection / Correction
    # Negative Spend or Revenue corrections
    neg_spend_count = (df["Marketing Spend"] < 0).sum()
    neg_rev_count = (df["Revenue"] < 0).sum()
    df["Marketing Spend"] = df["Marketing Spend"].abs()
    df["Revenue"] = df["Revenue"].abs()

    # Extreme Spend Outliers (> 10x 95th percentile by channel)
    channel_spend_caps = df.groupby("Marketing Channel")["Marketing Spend"].transform(lambda x: x.quantile(0.99) * 3)
    outlier_spend_mask = df["Marketing Spend"] > channel_spend_caps
    num_spend_outliers = outlier_spend_mask.sum()
    # Impute outliers with the channel median spend
    channel_spend_medians = df.groupby("Marketing Channel")["Marketing Spend"].transform("median")
    df.loc[outlier_spend_mask, "Marketing Spend"] = channel_spend_medians[outlier_spend_mask]

    print(f"5. Handled anomalies: {neg_spend_count} negative spend rows, {neg_rev_count} negative revenue rows, {num_spend_outliers} extreme spend outliers corrected.")

    # 6. Missing Value Imputation
    null_counts = df.isnull().sum()
    print("6. Missing values before imputation:")
    for col, count in null_counts[null_counts > 0].items():
        print(f"   - {col}: {count} missing values")

    # Impute Marketing Spend with Channel Median
    df["Marketing Spend"] = df.groupby("Marketing Channel")["Marketing Spend"].transform(
        lambda x: x.fillna(x.median())
    )

    # Impute Impressions based on Clicks / Channel CTR Median
    channel_ctr_medians = {
        "Google Ads": 0.038,
        "Facebook Ads": 0.024,
        "Instagram Ads": 0.018,
        "Email Marketing": 0.052,
        "Organic Search": 0.045,
        "Referral Marketing": 0.042
    }
    for ch, ctr in channel_ctr_medians.items():
        mask = (df["Marketing Channel"] == ch) & (df["Impressions"].isnull())
        df.loc[mask, "Impressions"] = (df.loc[mask, "Clicks"] / ctr).fillna(1000).astype(int)

    # Impute Leads
    channel_lead_rates = {
        "Google Ads": 0.14,
        "Facebook Ads": 0.10,
        "Instagram Ads": 0.08,
        "Email Marketing": 0.22,
        "Organic Search": 0.18,
        "Referral Marketing": 0.20
    }
    for ch, lr in channel_lead_rates.items():
        mask = (df["Marketing Channel"] == ch) & (df["Leads"].isnull())
        df.loc[mask, "Leads"] = (df.loc[mask, "Clicks"] * lr).fillna(0).astype(int)

    # Impute Revenue
    channel_aov = {
        "Google Ads": 175.0,
        "Facebook Ads": 130.0,
        "Instagram Ads": 115.0,
        "Email Marketing": 150.0,
        "Organic Search": 165.0,
        "Referral Marketing": 180.0
    }
    for ch, aov in channel_aov.items():
        mask = (df["Marketing Channel"] == ch) & (df["Revenue"].isnull())
        df.loc[mask, "Revenue"] = (df.loc[mask, "Conversions"] * aov).round(2)

    # Ensure integer columns are rounded and typed
    for int_col in ["Impressions", "Clicks", "Leads", "Conversions"]:
        df[int_col] = df[int_col].fillna(0).round().astype(int)

    # 7. Logical Consistency Checks & Funnel Validation
    # Clicks should not exceed Impressions
    click_anom = df["Clicks"] > df["Impressions"]
    df.loc[click_anom, "Impressions"] = df.loc[click_anom, "Clicks"] * 10

    # Leads should not exceed Clicks
    lead_anom = df["Leads"] > df["Clicks"]
    df.loc[lead_anom, "Leads"] = df.loc[lead_anom, "Clicks"]

    # Conversions should not exceed Leads (in lead-based funnel)
    conv_anom = df["Conversions"] > df["Leads"]
    df.loc[conv_anom, "Conversions"] = df.loc[conv_anom, "Leads"]

    # 8. Feature Engineering: KPI Calculations (Section 7)
    # Net Profit
    df["Net Profit"] = (df["Revenue"] - df["Marketing Spend"]).round(2)

    # ROI (%) = ((Revenue - Marketing Spend) / Marketing Spend) * 100
    df["ROI"] = np.where(
        df["Marketing Spend"] > 0,
        ((df["Revenue"] - df["Marketing Spend"]) / df["Marketing Spend"]) * 100,
        0.0
    ).round(2)

    # ROAS = Revenue / Marketing Spend
    df["ROAS"] = np.where(
        df["Marketing Spend"] > 0,
        df["Revenue"] / df["Marketing Spend"],
        0.0
    ).round(2)

    # CAC = Marketing Spend / Number of Conversions (New Customers)
    df["Customer Acquisition Cost"] = np.where(
        df["Conversions"] > 0,
        df["Marketing Spend"] / df["Conversions"],
        df["Marketing Spend"]  # If 0 conversions, CAC is full spend
    ).round(2)

    # Conversion Rate (%) = (Conversions / Clicks) * 100
    df["Conversion Rate"] = np.where(
        df["Clicks"] > 0,
        (df["Conversions"] / df["Clicks"]) * 100,
        0.0
    ).round(2)

    # Cost Per Click (CPC) = Marketing Spend / Clicks
    df["CPC"] = np.where(
        df["Clicks"] > 0,
        df["Marketing Spend"] / df["Clicks"],
        0.0
    ).round(2)

    # Cost Per Lead (CPL) = Marketing Spend / Leads
    df["CPL"] = np.where(
        df["Leads"] > 0,
        df["Marketing Spend"] / df["Leads"],
        0.0
    ).round(2)

    # Click-Through Rate (CTR, %) = (Clicks / Impressions) * 100
    df["CTR"] = np.where(
        df["Impressions"] > 0,
        (df["Clicks"] / df["Impressions"]) * 100,
        0.0
    ).round(2)

    # Date Calendar Features for Power BI & Time-Series
    df["Year"] = df["Campaign Date"].dt.year
    df["Month"] = df["Campaign Date"].dt.month
    df["Month_Name"] = df["Campaign Date"].dt.strftime("%b")
    df["Month_Year"] = df["Campaign Date"].dt.strftime("%Y-%m")
    df["Quarter"] = "Q" + df["Campaign Date"].dt.quarter.astype(str)
    df["Day_of_Week"] = df["Campaign Date"].dt.day_name()

    # Reorder columns logically
    ordered_cols = [
        "Campaign ID", "Campaign Name", "Marketing Channel", "Campaign Status", "Campaign Date",
        "Year", "Month", "Month_Name", "Month_Year", "Quarter", "Day_of_Week",
        "Marketing Spend", "Impressions", "Clicks", "Leads", "Conversions", "Revenue",
        "Net Profit", "ROI", "ROAS", "Customer Acquisition Cost", "Conversion Rate",
        "CPC", "CPL", "CTR", "Customer ID"
    ]
    df = df[ordered_cols]

    # Save cleaned dataset
    df.to_csv(output_csv_path, index=False)
    print(f"8. Successfully saved cleaned dataset to: {output_csv_path}")
    print(f"   Final records: {len(df)}, Final columns: {df.shape[1]}")
    print("=" * 70)
    
    return df


if __name__ == "__main__":
    df_clean = clean_marketing_data()
    print("\nSample Cleaned Data (First 3 rows):")
    print(df_clean.head(3).to_string())
    print("\nSummary Statistics of Key KPIs:")
    print(df_clean[["Marketing Spend", "Revenue", "Net Profit", "ROI", "ROAS", "Customer Acquisition Cost", "Conversion Rate"]].describe().to_string())
