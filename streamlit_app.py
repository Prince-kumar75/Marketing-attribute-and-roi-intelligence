"""
Marketing Attribution & ROI Intelligence - Streamlit Web Application
Ready for 1-click deployment on Streamlit Community Cloud (share.streamlit.io)
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

# Page Configuration
st.set_page_config(
    page_title="Marketing Attribution & ROI Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #1e3a8a;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/marketing_campaign_data_cleaned.csv")
    df["Campaign Date"] = pd.to_datetime(df["Campaign Date"])
    df_attr = pd.read_csv("data/processed/marketing_attribution_summary.csv")
    df_monthly = pd.read_csv("data/processed/monthly_channel_summary.csv")
    return df, df_attr, df_monthly

try:
    df, df_attr, df_monthly = load_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# Sidebar Navigation & Slicers
st.sidebar.title("📊 ROI Intelligence")
st.sidebar.caption("Marketing Attribution Platform")

nav_choice = st.sidebar.radio(
    "Navigation View",
    ["📈 Executive Overview", "🎯 Channel Performance", "🚀 Campaign Analysis", "🔀 Attribution Models"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters / Slicers")

channels = ["All Channels"] + sorted(list(df["Marketing Channel"].unique()))
selected_channel = st.sidebar.selectbox("Marketing Channel", channels)

statuses = ["All Statuses"] + sorted(list(df["Campaign Status"].unique()))
selected_status = st.sidebar.selectbox("Campaign Status", statuses)

# Filter Data
filtered_df = df.copy()
if selected_channel != "All Channels":
    filtered_df = filtered_df[filtered_df["Marketing Channel"] == selected_channel]
if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["Campaign Status"] == selected_status]

# -------------------------------------------------------------
# 1. Executive Overview
# -------------------------------------------------------------
if nav_choice == "📈 Executive Overview":
    st.title("📈 Executive Overview")
    st.markdown("High-level digital marketing spend, revenue generation, and portfolio ROI metrics.")

    # High-level KPIs
    tot_spend = filtered_df["Marketing Spend"].sum()
    tot_rev = filtered_df["Revenue"].sum()
    tot_profit = filtered_df["Net Profit"].sum()
    roas = tot_rev / tot_spend if tot_spend > 0 else 0
    roi = ((tot_rev - tot_spend) / tot_spend) * 100 if tot_spend > 0 else 0
    conversions = filtered_df["Conversions"].sum()
    leads = filtered_df["Leads"].sum()
    cac = tot_spend / conversions if conversions > 0 else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Spend", f"${tot_spend:,.0f}")
    col2.metric("Total Revenue", f"${tot_rev:,.0f}")
    col3.metric("Net Profit", f"${tot_profit:,.0f}")
    col4.metric("ROAS Multiple", f"{roas:.2f}x")
    col5.metric("Overall ROI", f"{roi:,.1f}%")
    col6.metric("Blended CAC", f"${cac:.2f}")

    st.markdown("---")
    
    # Monthly Spend vs Revenue
    st.subheader("Monthly Spend vs. Revenue Trajectory")
    monthly_agg = filtered_df.groupby(["Month", "Month_Name"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum"
    }).reset_index().sort_values("Month")
    monthly_agg["ROAS"] = monthly_agg["Revenue"] / monthly_agg["Marketing Spend"]

    st.bar_chart(monthly_agg.set_index("Month_Name")[["Marketing Spend", "Revenue"]])

    # Channel Matrix
    st.subheader("Executive Channel Performance Matrix")
    ch_matrix = filtered_df.groupby("Marketing Channel").agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index()
    ch_matrix["ROAS"] = (ch_matrix["Revenue"] / ch_matrix["Marketing Spend"]).round(2)
    ch_matrix["ROI (%)"] = (((ch_matrix["Revenue"] - ch_matrix["Marketing Spend"]) / ch_matrix["Marketing Spend"]) * 100).round(1)
    ch_matrix["CAC ($)"] = (ch_matrix["Marketing Spend"] / ch_matrix["Conversions"]).round(2)
    st.dataframe(ch_matrix.style.format({
        "Marketing Spend": "${:,.2f}",
        "Revenue": "${:,.2f}",
        "Net Profit": "${:,.2f}",
        "Conversions": "{:,}",
        "ROAS": "{:.2f}x",
        "ROI (%)": "{:,.1f}%",
        "CAC ($)": "${:.2f}"
    }), use_container_width=True)

# -------------------------------------------------------------
# 2. Channel Performance
# -------------------------------------------------------------
elif nav_choice == "🎯 Channel Performance":
    st.title("🎯 Channel Performance Diagnostic")
    st.markdown("Comparative channel efficiency, ROI multiples, and funnel conversion velocities.")

    ch_summary = filtered_df.groupby("Marketing Channel").agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Clicks": "sum",
        "Conversions": "sum"
    }).reset_index()
    ch_summary["ROAS"] = ch_summary["Revenue"] / ch_summary["Marketing Spend"]
    ch_summary["CAC"] = ch_summary["Marketing Spend"] / ch_summary["Conversions"]
    ch_summary["Conv_Rate"] = (ch_summary["Conversions"] / ch_summary["Clicks"]) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Return on Advertising Spend (ROAS)")
        st.bar_chart(ch_summary.set_index("Marketing Channel")["ROAS"])
    with col2:
        st.subheader("Customer Acquisition Cost (CAC)")
        st.bar_chart(ch_summary.set_index("Marketing Channel")["CAC"])

# -------------------------------------------------------------
# 3. Campaign Analysis
# -------------------------------------------------------------
elif nav_choice == "🚀 Campaign Analysis":
    st.title("🚀 Campaign Performance Leaderboards")
    st.markdown("Granular audit of top star performers and underperforming budget bleeders.")

    camp_perf = filtered_df.groupby(["Campaign ID", "Campaign Name", "Marketing Channel"]).agg({
        "Marketing Spend": "sum",
        "Revenue": "sum",
        "Net Profit": "sum",
        "Conversions": "sum"
    }).reset_index()
    camp_perf["ROAS"] = (camp_perf["Revenue"] / camp_perf["Marketing Spend"]).round(2)
    camp_perf["CAC"] = (camp_perf["Marketing Spend"] / camp_perf["Conversions"]).round(2)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Top 10 Profitable Campaigns")
        top10 = camp_perf.sort_values(by="Net Profit", ascending=False).head(10)
        st.dataframe(top10[["Campaign Name", "Marketing Channel", "Net Profit", "ROAS"]].style.format({
            "Net Profit": "${:,.2f}",
            "ROAS": "{:.2f}x"
        }), use_container_width=True)

    with col2:
        st.subheader("⚠️ Lowest Performing Campaigns (Budget Bleeders)")
        bottom10 = camp_perf.sort_values(by="ROAS", ascending=True).head(10)
        st.dataframe(bottom10[["Campaign Name", "Marketing Channel", "Marketing Spend", "ROAS", "CAC"]].style.format({
            "Marketing Spend": "${:,.2f}",
            "ROAS": "{:.2f}x",
            "CAC": "${:.2f}"
        }), use_container_width=True)

# -------------------------------------------------------------
# 4. Attribution Models
# -------------------------------------------------------------
elif nav_choice == "🔀 Attribution Models":
    st.title("🔀 Multi-Touch Marketing Attribution Analysis")
    st.info("💡 **Key Finding:** Single-touch Last-Touch models over-attribute bottom-of-funnel closers like Google Ads (+24.1% shift) and Email (+12.6% shift), while severely undervaluing top-of-funnel discovery channels like Facebook Ads (-15.6% shift) and Organic Search (-17.2% shift). Position-Based (40-40-20) provides an equitable balance.")

    attr_df = df_attr[df_attr["Marketing Channel"] != "Total"].copy()

    st.subheader("Attribution Model Revenue Comparison")
    st.bar_chart(attr_df.set_index("Marketing Channel")[["First_Touch_Revenue", "Last_Touch_Revenue", "Linear_Revenue", "Position_Based_Revenue"]])

    st.subheader("Attribution Model Allocation Table")
    st.dataframe(attr_df[[
        "Marketing Channel",
        "First_Touch_Revenue", "First_Touch_Revenue_Share_Pct",
        "Last_Touch_Revenue", "Last_Touch_Revenue_Share_Pct",
        "Linear_Revenue", "Linear_Revenue_Share_Pct",
        "Position_Based_Revenue", "Position_Based_Revenue_Share_Pct"
    ]].style.format({
        "First_Touch_Revenue": "${:,.2f}",
        "First_Touch_Revenue_Share_Pct": "{:.1f}%",
        "Last_Touch_Revenue": "${:,.2f}",
        "Last_Touch_Revenue_Share_Pct": "{:.1f}%",
        "Linear_Revenue": "${:,.2f}",
        "Linear_Revenue_Share_Pct": "{:.1f}%",
        "Position_Based_Revenue": "${:,.2f}",
        "Position_Based_Revenue_Share_Pct": "{:.1f}%"
    }), use_container_width=True)
