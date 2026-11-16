"""
Dashboard Data Exporter
Exports aggregated campaign and attribution data to dashboard/dashboard_data.js
for zero-friction browser execution without CORS restrictions.
"""

import pandas as pd
import json

def export_data():
    df = pd.read_csv("data/processed/marketing_campaign_data_cleaned.csv")
    df_attr = pd.read_csv("data/processed/marketing_attribution_summary.csv")
    df_monthly = pd.read_csv("data/processed/monthly_channel_summary.csv")

    # High-level KPIs
    total_spend = float(df["Marketing Spend"].sum())
    total_rev = float(df["Revenue"].sum())
    total_profit = float(df["Net Profit"].sum())
    total_conv = int(df["Conversions"].sum())
    total_leads = int(df["Leads"].sum())
    total_clicks = int(df["Clicks"].sum())
    total_impr = int(df["Impressions"].sum())

    kpis = {
        "total_spend": round(total_spend, 2),
        "total_revenue": round(total_rev, 2),
        "net_profit": round(total_profit, 2),
        "roas": round(total_rev / total_spend, 2),
        "roi_pct": round(((total_rev - total_spend) / total_spend) * 100, 2),
        "conversions": total_conv,
        "leads": total_leads,
        "clicks": total_clicks,
        "impressions": total_impr,
        "cac": round(total_spend / total_conv, 2),
        "cpc": round(total_spend / total_clicks, 2),
        "cpl": round(total_spend / total_leads, 2),
        "ctr": round((total_clicks / total_impr) * 100, 2),
        "conversion_rate": round((total_conv / total_clicks) * 100, 2)
    }

    # Channel Aggregates
    ch_df = df.groupby("Marketing Channel").agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Clicks": "sum",
        "Impressions": "sum",
        "Leads": "sum",
        "Conversions": "sum"
    }).reset_index()
    ch_df["roas"] = (ch_df["Revenue"] / ch_df["Marketing Spend"]).round(2)
    ch_df["roi_pct"] = (((ch_df["Revenue"] - ch_df["Marketing Spend"]) / ch_df["Marketing Spend"]) * 100).round(2)
    ch_df["cac"] = (ch_df["Marketing Spend"] / ch_df["Conversions"]).round(2)
    ch_df["cpc"] = (ch_df["Marketing Spend"] / ch_df["Clicks"]).round(2)
    ch_df["conv_rate"] = ((ch_df["Conversions"] / ch_df["Clicks"]) * 100).round(2)
    ch_df["ctr"] = ((ch_df["Clicks"] / ch_df["Impressions"]) * 100).round(2)
    channels_data = ch_df.to_dict(orient="records")

    # Monthly Trends
    monthly = df.groupby(["Month", "Month_Name"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index().sort_values("Month")
    monthly["roas"] = (monthly["Revenue"] / monthly["Marketing Spend"]).round(2)
    monthly_data = monthly.to_dict(orient="records")

    # Campaign Leaderboards
    camp_agg = df.groupby(["Campaign ID", "Campaign Name", "Marketing Channel", "Campaign Status"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index()
    camp_agg["roas"] = (camp_agg["Revenue"] / camp_agg["Marketing Spend"]).round(2)
    camp_agg["cac"] = (camp_agg["Marketing Spend"] / camp_agg["Conversions"]).round(2)

    top_campaigns = camp_agg.sort_values(by="Net Profit", ascending=False).head(10).to_dict(orient="records")
    bottom_campaigns = camp_agg.sort_values(by="roas", ascending=True).head(10).to_dict(orient="records")

    # Attribution Data
    attr_channels = df_attr[df_attr["Marketing Channel"] != "Total"].to_dict(orient="records")

    payload = {
        "kpis": kpis,
        "channels": channels_data,
        "monthly": monthly_data,
        "top_campaigns": top_campaigns,
        "bottom_campaigns": bottom_campaigns,
        "attribution": attr_channels
    }

    js_content = f"window.DASHBOARD_DATA = {json.dumps(payload, indent=2)};"
    with open("dashboard/dashboard_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Exported dashboard data to dashboard/dashboard_data.js")

if __name__ == "__main__":
    export_data()
