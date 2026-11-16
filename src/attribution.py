"""
Marketing Attribution Engine
Implements and compares:
- First-Touch Attribution
- Last-Touch Attribution
- Linear Attribution
- Position-Based (U-Shaped 40-40-20) Attribution
- Time-Decay Attribution (7-day half-life)
"""

import numpy as np
import pandas as pd


def compute_attribution_weights(df_touch):
    """
    Computes attribution weights for each touchpoint in each customer journey.
    """
    print("Computing attribution weights for customer journeys...")
    
    # Filter only converted customer journeys
    converted_journeys = df_touch[df_touch["Journey Converted"] == 1].copy()
    
    # Sort chronologically
    converted_journeys["Touchpoint Timestamp"] = pd.to_datetime(converted_journeys["Touchpoint Timestamp"])
    converted_journeys = converted_journeys.sort_values(
        by=["Customer ID", "Touchpoint Sequence"]
    ).reset_index(drop=True)

    # Initialize model weights
    converted_journeys["First_Touch_Weight"] = 0.0
    converted_journeys["Last_Touch_Weight"] = 0.0
    converted_journeys["Linear_Weight"] = 0.0
    converted_journeys["Position_Based_Weight"] = 0.0
    converted_journeys["Time_Decay_Weight"] = 0.0

    # Group by customer
    grouped = converted_journeys.groupby("Customer ID")

    first_touch_weights = []
    last_touch_weights = []
    linear_weights = []
    position_weights = []
    time_decay_weights = []

    for cust_id, group in grouped:
        n = len(group)
        indices = group.index

        # 1. First-Touch: 100% to touchpoint 1
        ft = np.zeros(n)
        ft[0] = 1.0

        # 2. Last-Touch: 100% to touchpoint n
        lt = np.zeros(n)
        lt[-1] = 1.0

        # 3. Linear: 1/n to all touchpoints
        lin = np.full(n, 1.0 / n)

        # 4. Position-Based (U-Shaped 40-40-20):
        # 1 touch: 1.0
        # 2 touches: 0.5, 0.5
        # >= 3 touches: 0.4 first, 0.4 last, 0.2 split among middle
        pos = np.zeros(n)
        if n == 1:
            pos[0] = 1.0
        elif n == 2:
            pos[0] = 0.5
            pos[1] = 0.5
        else:
            pos[0] = 0.40
            pos[-1] = 0.40
            middle_count = n - 2
            pos[1:-1] = 0.20 / middle_count

        # 5. Time-Decay (7-day half-life exponential decay)
        # Weight = 2 ^ (-delta_days / 7)
        conv_time = group["Touchpoint Timestamp"].iloc[-1]
        days_diff = (conv_time - group["Touchpoint Timestamp"]).dt.total_seconds() / (24 * 3600.0)
        half_life_days = 7.0
        decay_raw = np.power(2.0, -days_diff / half_life_days)
        time_decay = decay_raw / decay_raw.sum()

        for idx, i in enumerate(indices):
            converted_journeys.loc[i, "First_Touch_Weight"] = ft[idx]
            converted_journeys.loc[i, "Last_Touch_Weight"] = lt[idx]
            converted_journeys.loc[i, "Linear_Weight"] = lin[idx]
            converted_journeys.loc[i, "Position_Based_Weight"] = pos[idx]
            converted_journeys.loc[i, "Time_Decay_Weight"] = time_decay.iloc[idx]

    # Calculate Attributed Conversions & Attributed Revenue
    for model in ["First_Touch", "Last_Touch", "Linear", "Position_Based", "Time_Decay"]:
        w_col = f"{model}_Weight"
        converted_journeys[f"{model}_Conversions"] = converted_journeys[w_col] * 1.0
        converted_journeys[f"{model}_Revenue"] = (converted_journeys[w_col] * converted_journeys["Total Journey Revenue"]).round(2)

    return converted_journeys


def summarize_attribution(modeled_df, output_summary_path="data/processed/marketing_attribution_summary.csv"):
    """
    Aggregates conversions and revenue by marketing channel across all models.
    """
    models = ["First_Touch", "Last_Touch", "Linear", "Position_Based", "Time_Decay"]
    
    records = []
    channels = sorted(modeled_df["Marketing Channel"].unique())

    total_conversions = modeled_df["Journey Converted"].groupby(modeled_df["Customer ID"]).first().sum()
    total_revenue = modeled_df["Total Journey Revenue"].groupby(modeled_df["Customer ID"]).first().sum()

    for ch in channels:
        ch_df = modeled_df[modeled_df["Marketing Channel"] == ch]
        row = {"Marketing Channel": ch}
        
        for m in models:
            conv = ch_df[f"{m}_Conversions"].sum()
            rev = ch_df[f"{m}_Revenue"].sum()
            row[f"{m}_Conversions"] = round(conv, 1)
            row[f"{m}_Conversions_Share_Pct"] = round((conv / total_conversions) * 100, 2)
            row[f"{m}_Revenue"] = round(rev, 2)
            row[f"{m}_Revenue_Share_Pct"] = round((rev / total_revenue) * 100, 2)

        records.append(row)

    df_summary = pd.DataFrame(records)
    
    # Add Total Row
    total_row = {"Marketing Channel": "Total"}
    for m in models:
        total_row[f"{m}_Conversions"] = round(df_summary[f"{m}_Conversions"].sum(), 1)
        total_row[f"{m}_Conversions_Share_Pct"] = 100.0
        total_row[f"{m}_Revenue"] = round(df_summary[f"{m}_Revenue"].sum(), 2)
        total_row[f"{m}_Revenue_Share_Pct"] = 100.0
    
    df_summary = pd.concat([df_summary, pd.DataFrame([total_row])], ignore_index=True)
    df_summary.to_csv(output_summary_path, index=False)
    print(f"Attribution summary successfully saved to: {output_summary_path}")
    return df_summary


if __name__ == "__main__":
    df_touch = pd.read_csv("data/processed/customer_attribution_touchpoints.csv")
    print(f"Loaded touchpoints: {len(df_touch)} records.")
    
    df_modeled = compute_attribution_weights(df_touch)
    df_modeled.to_csv("data/processed/customer_attribution_modeled.csv", index=False)
    print(f"Saved modeled journey data to: data/processed/customer_attribution_modeled.csv")
    
    summary_df = summarize_attribution(df_modeled)
    print("\n" + "=" * 95)
    print("MARKETING ATTRIBUTION MODEL COMPARISON TABLE (REVENUE BY CHANNEL)")
    print("=" * 95)
    display_cols = [
        "Marketing Channel",
        "First_Touch_Revenue", "First_Touch_Revenue_Share_Pct",
        "Last_Touch_Revenue", "Last_Touch_Revenue_Share_Pct",
        "Linear_Revenue", "Linear_Revenue_Share_Pct",
        "Position_Based_Revenue", "Position_Based_Revenue_Share_Pct"
    ]
    print(summary_df[display_cols].to_string(index=False))
