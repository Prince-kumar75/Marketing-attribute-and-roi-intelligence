"""
Marketing Campaign Data Generator
Generates realistic multi-channel digital marketing campaign data and
customer multi-touch journey touchpoints for attribution modeling.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

CHANNELS = [
    "Google Ads",
    "Facebook Ads",
    "Instagram Ads",
    "Email Marketing",
    "Organic Search",
    "Referral Marketing",
]

CAMPAIGN_THEMES = {
    "Google Ads": [
        "Search_Brand_Core", "Search_High_Intent_Keywords", "Search_Competitor_Conquesting",
        "Performance_Max_Shopping", "Search_Long_Tail_Solutions", "Display_Remarketing_Banner"
    ],
    "Facebook Ads": [
        "Feed_Lookalike_Audience_1pct", "Feed_Prospecting_Interests", "Retargeting_Cart_Abandoners",
        "Video_Testimonials_Engagement", "Catalog_Dynamic_Product_Ads", "Lead_Gen_Form_Promo"
    ],
    "Instagram Ads": [
        "Stories_Influencer_Collab", "Reels_Product_Showcase", "Explore_Awareness_Campaign",
        "Feed_Visual_Storytelling", "Retargeting_Product_Carousel", "Holiday_Special_Stories"
    ],
    "Email Marketing": [
        "Welcome_Series_Drip", "Cart_Abandonment_Sequence", "VIP_Loyalty_Exclusive",
        "Weekly_Newsletter_Curated", "Re_Engagement_Winback", "Seasonal_Flash_Sale"
    ],
    "Organic Search": [
        "SEO_Comprehensive_Buying_Guides", "SEO_Category_Hub_Pages", "SEO_Product_Comparison_Articles",
        "SEO_Technical_Optimization", "SEO_How_To_Tutorials", "SEO_Top_10_Reviews"
    ],
    "Referral Marketing": [
        "Refer_A_Friend_Cashback", "Affiliate_Partner_Network", "Influencer_Ambassador_Program",
        "Loyalty_Tier_Perks", "Customer_Advocate_Rewards", "Partner_B2B_Cross_Promotion"
    ]
}

CHANNEL_METRICS = {
    "Google Ads": {
        "spend_range": (350, 1500),
        "cpc_range": (1.80, 4.50),
        "ctr_mean": 0.038,
        "lead_rate": 0.14,
        "conv_rate": 0.055,
        "aov_range": (110, 240),
        "status_weights": [0.70, 0.20, 0.10]  # Active, Completed, Paused
    },
    "Facebook Ads": {
        "spend_range": (250, 1200),
        "cpc_range": (0.90, 2.20),
        "ctr_mean": 0.024,
        "lead_rate": 0.10,
        "conv_rate": 0.035,
        "aov_range": (85, 180),
        "status_weights": [0.65, 0.25, 0.10]
    },
    "Instagram Ads": {
        "spend_range": (200, 1000),
        "cpc_range": (0.80, 1.90),
        "ctr_mean": 0.018,
        "lead_rate": 0.08,
        "conv_rate": 0.028,
        "aov_range": (75, 160),
        "status_weights": [0.65, 0.25, 0.10]
    },
    "Email Marketing": {
        "spend_range": (50, 300),
        "cpc_range": (0.15, 0.50),
        "ctr_mean": 0.052,
        "lead_rate": 0.22,
        "conv_rate": 0.085,
        "aov_range": (95, 210),
        "status_weights": [0.80, 0.15, 0.05]
    },
    "Organic Search": {
        "spend_range": (100, 450),
        "cpc_range": (0.10, 0.40),
        "ctr_mean": 0.045,
        "lead_rate": 0.18,
        "conv_rate": 0.062,
        "aov_range": (105, 225),
        "status_weights": [0.85, 0.10, 0.05]
    },
    "Referral Marketing": {
        "spend_range": (150, 600),
        "cpc_range": (0.60, 1.40),
        "ctr_mean": 0.042,
        "lead_rate": 0.20,
        "conv_rate": 0.070,
        "aov_range": (115, 250),
        "status_weights": [0.75, 0.15, 0.10]
    }
}


def generate_campaign_dataset(num_records=8500, start_date="2025-01-01", end_date="2025-12-31"):
    """Generates the main campaign performance dataset."""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    date_range_days = (end_dt - start_dt).days

    records = []
    
    # Pre-generate a pool of customer IDs
    num_unique_customers = 6000
    customer_pool = [f"CUST-{10000 + i}" for i in range(num_unique_customers)]

    # Campaign definitions
    all_campaigns = []
    camp_counter = 101
    for channel, themes in CAMPAIGN_THEMES.items():
        for theme in themes:
            all_campaigns.append({
                "campaign_id": f"CMP-{camp_counter}",
                "campaign_name": f"{channel.replace(' ', '_')}_{theme}",
                "channel": channel
            })
            camp_counter += 1

    for i in range(num_records):
        # Pick random campaign
        camp = random.choice(all_campaigns)
        channel = camp["channel"]
        metrics = CHANNEL_METRICS[channel]

        # Pick date with seasonal weighting (higher weight in Nov-Dec, July)
        day_offset = random.randint(0, date_range_days)
        rec_date = start_dt + timedelta(days=day_offset)
        
        month = rec_date.month
        seasonality = 1.0
        if month in [11, 12]:  # Holiday season
            seasonality = 1.45
        elif month in [7]:     # Summer flash sale
            seasonality = 1.25
        elif month in [1, 2]:  # Post holiday dip
            seasonality = 0.85

        # Base spend
        spend = np.random.uniform(metrics["spend_range"][0], metrics["spend_range"][1]) * seasonality
        spend = round(float(spend), 2)

        # CPC & Clicks
        cpc = np.random.uniform(metrics["cpc_range"][0], metrics["cpc_range"][1])
        clicks = int(max(1, np.random.normal(spend / cpc, (spend / cpc) * 0.15)))

        # Impressions based on CTR
        ctr = np.random.normal(metrics["ctr_mean"], metrics["ctr_mean"] * 0.20)
        ctr = max(0.005, min(0.12, ctr))
        impressions = int(max(clicks * 5, clicks / ctr))

        # Leads based on lead rate
        lead_rate = np.random.normal(metrics["lead_rate"], metrics["lead_rate"] * 0.20)
        lead_rate = max(0.02, min(0.40, lead_rate))
        leads = int(np.random.binomial(clicks, lead_rate))

        # Conversions based on conversion rate from clicks
        conv_rate = np.random.normal(metrics["conv_rate"], metrics["conv_rate"] * 0.25)
        conv_rate = max(0.008, min(0.20, conv_rate))
        conversions = int(np.random.binomial(clicks, conv_rate))
        
        # Revenue based on conversions & Average Order Value (AOV)
        if conversions > 0:
            aov = np.random.uniform(metrics["aov_range"][0], metrics["aov_range"][1]) * (1.1 if month in [11, 12] else 1.0)
            revenue = round(float(conversions * aov * np.random.uniform(0.9, 1.15)), 2)
            cac = round(float(spend / conversions), 2)
        else:
            revenue = 0.0
            cac = round(float(spend), 2)

        # Status
        statuses = ["Active", "Completed", "Paused"]
        status = np.random.choice(statuses, p=metrics["status_weights"])

        # Customer ID associated with the primary conversion/lead batch
        cust_id = random.choice(customer_pool)

        records.append({
            "Campaign ID": camp["campaign_id"],
            "Campaign Name": camp["campaign_name"],
            "Marketing Channel": channel,
            "Campaign Date": rec_date.strftime("%Y-%m-%d"),
            "Marketing Spend": spend,
            "Impressions": impressions,
            "Clicks": clicks,
            "Leads": leads,
            "Conversions": conversions,
            "Revenue": revenue,
            "Customer ID": cust_id,
            "Customer Acquisition Cost": cac,
            "Campaign Status": status
        })

    df = pd.DataFrame(records)
    return df


def inject_realistic_imperfections(df):
    """
    Injects realistic data quality issues for data cleaning demonstration:
    - Missing values (NaNs)
    - Duplicate rows
    - Inconsistent date formats
    - Inconsistent casing and whitespace
    - Erroneous / outlier entries
    """
    df_raw = df.copy()
    num_rows = len(df_raw)

    # 1. Duplicate rows (~120 duplicates)
    dup_indices = np.random.choice(num_rows, size=120, replace=False)
    dup_rows = df_raw.iloc[dup_indices].copy()
    df_raw = pd.concat([df_raw, dup_rows], ignore_index=True)

    # 2. Inconsistent Date formats
    # convert ~15% of dates to MM/DD/YYYY, and ~5% to DD-MM-YYYY
    dates = df_raw["Campaign Date"].values
    for idx in range(len(df_raw)):
        rand_val = random.random()
        if rand_val < 0.15:
            dt = datetime.strptime(dates[idx][:10], "%Y-%m-%d")
            dates[idx] = dt.strftime("%m/%d/%Y")
        elif rand_val < 0.20:
            dt = datetime.strptime(dates[idx][:10], "%Y-%m-%d")
            dates[idx] = dt.strftime("%d-%m-%Y")
    df_raw["Campaign Date"] = dates

    # 3. Missing values in numerical columns (~1.5% in Marketing Spend, Impressions, Leads, Revenue)
    for col in ["Marketing Spend", "Impressions", "Leads", "Revenue"]:
        nan_indices = np.random.choice(len(df_raw), size=int(len(df_raw) * 0.015), replace=False)
        df_raw.loc[nan_indices, col] = np.nan

    # 4. Inconsistent Channel Casing & Whitespace
    channel_col = df_raw["Marketing Channel"].values
    for idx in range(len(df_raw)):
        if random.random() < 0.05:
            ch = channel_col[idx]
            choice = random.choice([ch.lower(), ch.upper(), f"  {ch}  ", ch.replace("Ads", "ads")])
            channel_col[idx] = choice
    df_raw["Marketing Channel"] = channel_col

    # 5. Inconsistent Campaign Status
    status_col = df_raw["Campaign Status"].values
    for idx in range(len(df_raw)):
        if random.random() < 0.04:
            st = status_col[idx]
            status_col[idx] = random.choice([st.lower(), f" {st} ", st.upper()])
    df_raw["Campaign Status"] = status_col

    # 6. Outliers / erroneous values (~15 rows with negative values or extreme data entry errors)
    outlier_spend_idx = np.random.choice(len(df_raw), size=10, replace=False)
    df_raw.loc[outlier_spend_idx[:5], "Marketing Spend"] = -df_raw.loc[outlier_spend_idx[:5], "Marketing Spend"].abs()
    # High extreme spend anomaly
    df_raw.loc[outlier_spend_idx[5:], "Marketing Spend"] = df_raw.loc[outlier_spend_idx[5:], "Marketing Spend"] * 35

    outlier_rev_idx = np.random.choice(len(df_raw), size=5, replace=False)
    df_raw.loc[outlier_rev_idx, "Revenue"] = -df_raw.loc[outlier_rev_idx, "Revenue"].abs()

    # Shuffle the dataset
    df_raw = df_raw.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df_raw


def generate_attribution_touchpoints(num_customers=5000, start_date="2025-01-01", end_date="2025-12-31"):
    """
    Generates a realistic customer journey touchpoint dataset.
    Each customer interacts with 1 to 6 touchpoints across different channels
    over a 1-30 day window before either converting or abandoning.
    Enables First-Touch, Last-Touch, Linear, Position-Based (40-40-20), and Time-Decay attribution.
    """
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end_dt - start_dt).days

    touchpoint_records = []
    
    # Typical customer journey archetypes
    channel_roles = {
        "Organic Search": {"opener_prob": 0.35, "closer_prob": 0.15},
        "Facebook Ads": {"opener_prob": 0.30, "closer_prob": 0.10},
        "Instagram Ads": {"opener_prob": 0.20, "closer_prob": 0.08},
        "Google Ads": {"opener_prob": 0.10, "closer_prob": 0.40},
        "Email Marketing": {"opener_prob": 0.03, "closer_prob": 0.17},
        "Referral Marketing": {"opener_prob": 0.02, "closer_prob": 0.10}
    }

    channels_list = list(channel_roles.keys())
    open_weights = [channel_roles[c]["opener_prob"] for c in channels_list]
    close_weights = [channel_roles[c]["closer_prob"] for c in channels_list]

    for cust_idx in range(1, num_customers + 1):
        cust_id = f"CUST-{10000 + cust_idx}"
        
        # Decide journey length: 1 to 5 touchpoints
        # 30% single-touch, 70% multi-touch
        if random.random() < 0.30:
            num_touchpoints = 1
        else:
            num_touchpoints = random.choices([2, 3, 4, 5], weights=[0.40, 0.35, 0.18, 0.07])[0]

        # Base journey start date
        journey_start_day = random.randint(0, total_days - 35)
        journey_start_time = start_dt + timedelta(days=journey_start_day, hours=random.randint(8, 22))

        # Overall conversion probability for this customer
        # Multi-touch journeys convert at a higher rate
        base_conv_prob = 0.28 if num_touchpoints == 1 else (0.45 + (num_touchpoints * 0.07))
        has_converted = random.random() < min(0.85, base_conv_prob)
        
        conv_revenue = 0.0
        if has_converted:
            # Order value between $60 and $380
            conv_revenue = round(float(np.random.gamma(shape=5, scale=30) + 40), 2)

        current_time = journey_start_time

        for t_idx in range(num_touchpoints):
            touch_num = t_idx + 1
            
            # Select channel based on position in funnel
            if num_touchpoints == 1:
                ch = random.choices(channels_list, weights=open_weights)[0]
            elif t_idx == 0:  # First touch
                ch = random.choices(channels_list, weights=open_weights)[0]
            elif t_idx == num_touchpoints - 1:  # Last touch
                ch = random.choices(channels_list, weights=close_weights)[0]
            else:  # Middle touches
                ch = random.choice(channels_list)

            # Pick a campaign from this channel
            camp_theme = random.choice(CAMPAIGN_THEMES[ch])
            campaign_name = f"{ch.replace(' ', '_')}_{camp_theme}"

            # Time gap between touchpoints (e.g. 1-7 days)
            if t_idx > 0:
                hours_gap = random.randint(4, 120)
                current_time = current_time + timedelta(hours=hours_gap)

            is_conversion_touchpoint = 1 if (has_converted and t_idx == num_touchpoints - 1) else 0

            touchpoint_records.append({
                "Customer ID": cust_id,
                "Touchpoint Sequence": touch_num,
                "Total Touchpoints": num_touchpoints,
                "Touchpoint Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Touchpoint Date": current_time.strftime("%Y-%m-%d"),
                "Marketing Channel": ch,
                "Campaign Name": campaign_name,
                "Journey Converted": 1 if has_converted else 0,
                "Is Conversion Touchpoint": is_conversion_touchpoint,
                "Conversion Revenue": conv_revenue if is_conversion_touchpoint == 1 else 0.0,
                "Total Journey Revenue": conv_revenue
            })

    df_touch = pd.DataFrame(touchpoint_records)
    return df_touch


if __name__ == "__main__":
    print("Generating marketing campaign datasets...")
    df_clean_base = generate_campaign_dataset(num_records=8500)
    df_raw = inject_realistic_imperfections(df_clean_base)
    
    df_raw.to_csv("data/raw/marketing_campaign_data_raw.csv", index=False)
    print(f"Saved raw dataset: data/raw/marketing_campaign_data_raw.csv with {len(df_raw)} records.")

    print("Generating customer journey touchpoint dataset for attribution...")
    df_touch = generate_attribution_touchpoints(num_customers=5500)
    df_touch.to_csv("data/processed/customer_attribution_touchpoints.csv", index=False)
    print(f"Saved touchpoint dataset: data/processed/customer_attribution_touchpoints.csv with {len(df_touch)} touchpoints.")
