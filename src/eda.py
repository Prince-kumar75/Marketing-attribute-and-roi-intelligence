"""
Exploratory Data Analysis (EDA) and Visualization Module
Generates production-grade visualizations and summaries for marketing performance.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300


def run_eda(cleaned_csv_path="data/processed/marketing_campaign_data_cleaned.csv",
            attribution_summary_path="data/processed/marketing_attribution_summary.csv",
            output_fig_dir="reports/figures"):
    
    os.makedirs(output_fig_dir, exist_ok=True)
    df = pd.read_csv(cleaned_csv_path)
    df["Campaign Date"] = pd.to_datetime(df["Campaign Date"])
    
    print("=" * 70)
    print("EXECUTIVE MARKETING PERFORMANCE OVERVIEW")
    print("=" * 70)
    total_spend = df["Marketing Spend"].sum()
    total_rev = df["Revenue"].sum()
    total_profit = df["Net Profit"].sum()
    overall_roi = ((total_rev - total_spend) / total_spend) * 100
    overall_roas = total_rev / total_spend
    total_conv = df["Conversions"].sum()
    total_leads = df["Leads"].sum()
    total_clicks = df["Clicks"].sum()
    overall_cac = total_spend / total_conv
    overall_cpc = total_spend / total_clicks
    overall_cpl = total_spend / total_leads
    overall_conv_rate = (total_conv / total_clicks) * 100

    print(f"Total Marketing Spend:     ${total_spend:,.2f}")
    print(f"Total Revenue Generated:   ${total_rev:,.2f}")
    print(f"Total Net Profit:          ${total_profit:,.2f}")
    print(f"Overall Marketing ROI:     {overall_roi:.2f}%")
    print(f"Overall Portfolio ROAS:    {overall_roas:.2f}x")
    print(f"Total Conversions:         {total_conv:,}")
    print(f"Total Leads:               {total_leads:,}")
    print(f"Blended CAC:               ${overall_cac:.2f}")
    print(f"Blended CPC:               ${overall_cpc:.2f}")
    print(f"Blended Conversion Rate:   {overall_conv_rate:.2f}%")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Spend vs Revenue by Channel
    # -------------------------------------------------------------
    ch_agg = df.groupby("Marketing Channel").agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Clicks": "sum",
        "Leads": "sum",
        "Conversions": "sum"
    }).reset_index()
    ch_agg["ROI"] = ((ch_agg["Revenue"] - ch_agg["Marketing Spend"]) / ch_agg["Marketing Spend"]) * 100
    ch_agg["ROAS"] = ch_agg["Revenue"] / ch_agg["Marketing Spend"]
    ch_agg["CAC"] = ch_agg["Marketing Spend"] / ch_agg["Conversions"]
    ch_agg["Conv_Rate"] = (ch_agg["Conversions"] / ch_agg["Clicks"]) * 100
    ch_agg = ch_agg.sort_values(by="Revenue", ascending=False).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(ch_agg))
    width = 0.38
    
    bars1 = ax.bar(x - width/2, ch_agg["Marketing Spend"] / 1000, width, label="Marketing Spend ($k)", color="#3498db", edgecolor="#2980b9")
    bars2 = ax.bar(x + width/2, ch_agg["Revenue"] / 1000, width, label="Revenue ($k)", color="#2ecc71", edgecolor="#27ae60")
    
    ax.set_ylabel("Amount in Thousands (USD $k)", fontsize=12, fontweight="bold")
    ax.set_title("Marketing Spend vs. Revenue by Channel (Full Year 2025)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(ch_agg["Marketing Channel"], rotation=20, ha="right", fontsize=11)
    ax.legend(frameon=True, fontsize=11)
    
    # Value labels
    for bar in bars1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f"${yval:,.0f}k", ha='center', va='bottom', fontsize=9, rotation=0)
    for bar in bars2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f"${yval:,.0f}k", ha='center', va='bottom', fontsize=9, rotation=0, fontweight="bold")
    
    plt.tight_layout()
    fig1_path = os.path.join(output_fig_dir, "01_channel_spend_vs_revenue.png")
    plt.savefig(fig1_path)
    plt.close()
    print(f"Generated: {fig1_path}")

    # -------------------------------------------------------------
    # 2. Channel ROI & ROAS Comparison
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Sort for ROI
    ch_roi_sorted = ch_agg.sort_values(by="ROI", ascending=True)
    colors_roi = ["#e74c3c" if val < 500 else "#f39c12" if val < 1000 else "#27ae60" for val in ch_roi_sorted["ROI"]]
    bars_roi = ax1.barh(ch_roi_sorted["Marketing Channel"], ch_roi_sorted["ROI"], color=colors_roi)
    ax1.set_xlabel("Return on Investment (ROI %)", fontsize=12, fontweight="bold")
    ax1.set_title("Channel Return on Investment (ROI %)", fontsize=13, fontweight="bold")
    for bar in bars_roi:
        ax1.text(bar.get_width() + 40, bar.get_y() + bar.get_height()/2, f"{bar.get_width():,.1f}%", va='center', fontsize=10, fontweight="bold")

    # ROAS
    ch_roas_sorted = ch_agg.sort_values(by="ROAS", ascending=True)
    colors_roas = ["#3498db" if val < 10 else "#9b59b6" if val < 20 else "#16a085" for val in ch_roas_sorted["ROAS"]]
    bars_roas = ax2.barh(ch_roas_sorted["Marketing Channel"], ch_roas_sorted["ROAS"], color=colors_roas)
    ax2.set_xlabel("Return on Advertising Spend (ROAS x)", fontsize=12, fontweight="bold")
    ax2.set_title("Channel Return on Advertising Spend (ROAS Multiple)", fontsize=13, fontweight="bold")
    for bar in bars_roas:
        ax2.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}x", va='center', fontsize=10, fontweight="bold")

    plt.tight_layout()
    fig2_path = os.path.join(output_fig_dir, "02_channel_roi_roas_comparison.png")
    plt.savefig(fig2_path)
    plt.close()
    print(f"Generated: {fig2_path}")

    # -------------------------------------------------------------
    # 3. Monthly Spend, Revenue & ROAS Trends
    # -------------------------------------------------------------
    monthly_agg = df.groupby(["Year", "Month", "Month_Name", "Month_Year"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index().sort_values(by=["Year", "Month"]).reset_index(drop=True)
    monthly_agg["ROAS"] = monthly_agg["Revenue"] / monthly_agg["Marketing Spend"]
    monthly_agg["Revenue_Growth_MoM_Pct"] = monthly_agg["Revenue"].pct_change() * 100

    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    x_labels = monthly_agg["Month_Name"]
    ax1.plot(x_labels, monthly_agg["Marketing Spend"] / 1000, marker='o', linewidth=2.5, color="#e67e22", label="Spend ($k)")
    ax1.plot(x_labels, monthly_agg["Revenue"] / 1000, marker='s', linewidth=2.5, color="#27ae60", label="Revenue ($k)")
    ax1.fill_between(x_labels, monthly_agg["Revenue"] / 1000, monthly_agg["Marketing Spend"] / 1000, color="#2ecc71", alpha=0.15, label="Net Profit Margin")
    ax1.set_ylabel("Monthly Amount ($k USD)", fontsize=12, fontweight="bold", color="#2c3e50")
    ax1.set_title("Monthly Marketing Expenditure vs. Revenue Trends (2025)", fontsize=14, fontweight="bold", pad=15)
    
    # Secondary axis for ROAS
    ax2 = ax1.twinx()
    ax2.plot(x_labels, monthly_agg["ROAS"], marker='^', linewidth=2, linestyle='--', color="#8e44ad", label="ROAS Multiple (x)")
    ax2.set_ylabel("ROAS (x)", fontsize=12, fontweight="bold", color="#8e44ad")
    ax2.grid(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

    plt.tight_layout()
    fig3_path = os.path.join(output_fig_dir, "03_monthly_revenue_and_spend_trends.png")
    plt.savefig(fig3_path)
    plt.close()
    print(f"Generated: {fig3_path}")

    # -------------------------------------------------------------
    # 4. Marketing Attribution Model Comparison
    # -------------------------------------------------------------
    df_attr = pd.read_csv(attribution_summary_path)
    # Exclude Total row
    df_attr_ch = df_attr[df_attr["Marketing Channel"] != "Total"].copy()

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(df_attr_ch))
    width = 0.20

    m1 = ax.bar(x - 1.5*width, df_attr_ch["First_Touch_Revenue_Share_Pct"], width, label="First-Touch", color="#3498db")
    m2 = ax.bar(x - 0.5*width, df_attr_ch["Last_Touch_Revenue_Share_Pct"], width, label="Last-Touch", color="#e74c3c")
    m3 = ax.bar(x + 0.5*width, df_attr_ch["Linear_Revenue_Share_Pct"], width, label="Linear", color="#f39c12")
    m4 = ax.bar(x + 1.5*width, df_attr_ch["Position_Based_Revenue_Share_Pct"], width, label="Position-Based (40-40-20)", color="#2ecc71")

    ax.set_ylabel("Revenue Share (%)", fontsize=12, fontweight="bold")
    ax.set_title("Attribution Model Comparison: Revenue Share Distribution Across Channels", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(df_attr_ch["Marketing Channel"], rotation=20, ha="right", fontsize=11)
    ax.legend(frameon=True, fontsize=11)

    plt.tight_layout()
    fig4_path = os.path.join(output_fig_dir, "04_attribution_model_comparison.png")
    plt.savefig(fig4_path)
    plt.close()
    print(f"Generated: {fig4_path}")

    # -------------------------------------------------------------
    # 5. Customer Acquisition Cost (CAC) vs Cost Per Click (CPC)
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    ch_cac_sorted = ch_agg.sort_values(by="CAC", ascending=True)
    bars_cac = ax1.barh(ch_cac_sorted["Marketing Channel"], ch_cac_sorted["CAC"], color="#e67e22")
    ax1.set_xlabel("Customer Acquisition Cost ($ / Conversion)", fontsize=11, fontweight="bold")
    ax1.set_title("Customer Acquisition Cost (CAC) by Channel", fontsize=13, fontweight="bold")
    for bar in bars_cac:
        ax1.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height()/2, f"${bar.get_width():.2f}", va='center', fontsize=10, fontweight="bold")

    ch_cpc_sorted = ch_agg.assign(CPC=ch_agg["Marketing Spend"] / ch_agg["Clicks"]).sort_values(by="CPC", ascending=True)
    bars_cpc = ax2.barh(ch_cpc_sorted["Marketing Channel"], ch_cpc_sorted["CPC"], color="#16a085")
    ax2.set_xlabel("Cost Per Click ($ / Click)", fontsize=11, fontweight="bold")
    ax2.set_title("Cost Per Click (CPC) by Channel", fontsize=13, fontweight="bold")
    for bar in bars_cpc:
        ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f"${bar.get_width():.2f}", va='center', fontsize=10, fontweight="bold")

    plt.tight_layout()
    fig5_path = os.path.join(output_fig_dir, "05_cac_and_cpc_by_channel.png")
    plt.savefig(fig5_path)
    plt.close()
    print(f"Generated: {fig5_path}")

    # -------------------------------------------------------------
    # 6. Funnel Efficiency Metrics
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ch_funnel = ch_agg.assign(
        CTR=(ch_agg["Clicks"] / df.groupby("Marketing Channel")["Impressions"].sum().values) * 100,
        Lead_Rate=(ch_agg["Leads"] / ch_agg["Clicks"]) * 100,
        Conv_Rate=(ch_agg["Conversions"] / ch_agg["Clicks"]) * 100
    )
    x = np.arange(len(ch_funnel))
    width = 0.25
    ax.bar(x - width, ch_funnel["CTR"], width, label="CTR (Clicks / Impr %)", color="#3498db")
    ax.bar(x, ch_funnel["Lead_Rate"], width, label="Lead Rate (Leads / Clicks %)", color="#f39c12")
    ax.bar(x + width, ch_funnel["Conv_Rate"], width, label="Conversion Rate (Conv / Clicks %)", color="#2ecc71")
    ax.set_ylabel("Efficiency Rate (%)", fontsize=12, fontweight="bold")
    ax.set_title("Conversion Funnel Velocity by Marketing Channel", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(ch_funnel["Marketing Channel"], rotation=20, ha="right", fontsize=11)
    ax.legend(frameon=True, fontsize=11)

    plt.tight_layout()
    fig6_path = os.path.join(output_fig_dir, "06_conversion_funnel_rates.png")
    plt.savefig(fig6_path)
    plt.close()
    print(f"Generated: {fig6_path}")

    # -------------------------------------------------------------
    # 7. Campaign Profitability Matrix
    # -------------------------------------------------------------
    camp_summary = df.groupby(["Campaign ID", "Campaign Name", "Marketing Channel"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index()
    camp_summary["ROAS"] = camp_summary["Revenue"] / camp_summary["Marketing Spend"]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    scatter = ax.scatter(
        camp_summary["Marketing Spend"] / 1000,
        camp_summary["Revenue"] / 1000,
        c=camp_summary["ROAS"],
        cmap="viridis",
        s=camp_summary["Conversions"] * 0.12,
        alpha=0.75,
        edgecolors="black",
        linewidth=0.7
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("ROAS Multiple (Revenue / Spend)", fontsize=11, fontweight="bold")
    ax.set_xlabel("Campaign Total Spend ($k)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Campaign Total Revenue ($k)", fontsize=12, fontweight="bold")
    ax.set_title("Campaign Profitability & Efficiency Matrix (Bubble Size = Total Conversions)", fontsize=14, fontweight="bold", pad=15)

    # Highlight top profitable campaigns
    top_camps = camp_summary.nlargest(3, "Net Profit")
    for _, r in top_camps.iterrows():
        ax.annotate(
            r["Campaign Name"].split("_", 2)[-1][:20],
            (r["Marketing Spend"] / 1000, r["Revenue"] / 1000),
            xytext=(10, 10), textcoords="offset points",
            fontweight="bold", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.6)
        )

    plt.tight_layout()
    fig7_path = os.path.join(output_fig_dir, "07_campaign_profitability_matrix.png")
    plt.savefig(fig7_path)
    plt.close()
    print(f"Generated: {fig7_path}")

    # -------------------------------------------------------------
    # 8. Channel Revenue Share Donut Chart
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 7))
    palette = ["#2ecc71", "#3498db", "#9b59b6", "#f39c12", "#e74c3c", "#1abc9c"]
    wedges, texts, autotexts = ax.pie(
        ch_agg["Revenue"],
        labels=ch_agg["Marketing Channel"],
        autopct='%1.1f%%',
        pctdistance=0.75,
        colors=palette,
        startangle=140,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=11)
    ax.set_title("Channel Share of Total Revenue (2025)", fontsize=14, fontweight="bold", pad=20)
    
    plt.tight_layout()
    fig8_path = os.path.join(output_fig_dir, "08_channel_revenue_share_pie.png")
    plt.savefig(fig8_path)
    plt.close()
    print(f"Generated: {fig8_path}")

    # Save monthly channel summary table
    monthly_channel_summary = df.groupby(["Year", "Month", "Month_Name", "Marketing Channel"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Clicks": "sum",
        "Leads": "sum",
        "Conversions": "sum"
    }).reset_index()
    monthly_channel_summary["ROI"] = ((monthly_channel_summary["Revenue"] - monthly_channel_summary["Marketing Spend"]) / monthly_channel_summary["Marketing Spend"]) * 100
    monthly_channel_summary["ROAS"] = monthly_channel_summary["Revenue"] / monthly_channel_summary["Marketing Spend"]
    monthly_channel_summary.to_csv("data/processed/monthly_channel_summary.csv", index=False)
    print("Saved monthly channel summary table: data/processed/monthly_channel_summary.csv")

    return ch_agg, monthly_agg, camp_summary


if __name__ == "__main__":
    ch_agg, monthly_agg, camp_summary = run_eda()
