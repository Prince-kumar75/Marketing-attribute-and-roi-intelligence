"""
SQL Analysis Execution Script
Loads cleaned datasets into SQLite, executes all business queries,
and exports verified query results to Markdown.
"""

import sqlite3
import pandas as pd
import os


def df_to_markdown(df):
    """Converts a pandas DataFrame to a clean markdown table string without tabulate."""
    headers = [str(c) for c in df.columns]
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        row_str = [str(val) for val in row.values]
        lines.append("| " + " | ".join(row_str) + " |")
    return "\n".join(lines)


def run_all_sql_queries():
    print("=" * 70)
    print("EXECUTING MARKETING SQL ANALYTICS QUERIES")
    print("=" * 70)

    # 1. Connect to SQLite DB
    conn = sqlite3.connect(":memory:")
    
    # 2. Ingest Cleaned Data
    df_campaigns = pd.read_csv("data/processed/marketing_campaign_data_cleaned.csv")
    df_touchpoints = pd.read_csv("data/processed/customer_attribution_touchpoints.csv")

    # Rename column names to snake_case for standard SQL queries
    df_campaigns.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in df_campaigns.columns]
    df_touchpoints.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in df_touchpoints.columns]

    df_campaigns.to_sql("marketing_campaigns", conn, index=False, if_exists="replace")
    df_touchpoints.to_sql("customer_attribution_touchpoints", conn, index=False, if_exists="replace")
    print(f"Loaded {len(df_campaigns)} campaign rows and {len(df_touchpoints)} touchpoints into SQLite.")

    queries = {
        "Query 1: Total Marketing Expenditure, Revenue, Profit & Portfolio ROI": """
            SELECT
                COUNT(*) AS total_campaign_records,
                ROUND(SUM(marketing_spend), 2) AS total_marketing_expenditure,
                ROUND(SUM(revenue), 2) AS total_revenue_generated,
                ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS total_net_profit,
                ROUND(((SUM(revenue) - SUM(marketing_spend)) / SUM(marketing_spend)) * 100.0, 2) AS overall_roi_percentage,
                ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS overall_portfolio_roas
            FROM marketing_campaigns;
        """,
        "Query 2: Total Revenue, Spend, Profit, and ROAS by Marketing Channel": """
            SELECT
                marketing_channel,
                COUNT(DISTINCT campaign_id) AS active_campaigns_count,
                ROUND(SUM(marketing_spend), 2) AS total_spend,
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS net_profit,
                ROUND(((SUM(revenue) - SUM(marketing_spend)) / SUM(marketing_spend)) * 100.0, 2) AS channel_roi_pct,
                ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS channel_roas,
                ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM marketing_campaigns), 2) AS pct_of_total_revenue
            FROM marketing_campaigns
            GROUP BY marketing_channel
            ORDER BY total_revenue DESC;
        """,
        "Query 3: Top 5 Profitable Campaigns": """
            SELECT
                campaign_id,
                campaign_name,
                marketing_channel,
                ROUND(SUM(marketing_spend), 2) AS total_spend,
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS net_profit,
                ROUND(((SUM(revenue) - SUM(marketing_spend)) / SUM(marketing_spend)) * 100.0, 2) AS roi_pct,
                ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS roas,
                SUM(conversions) AS total_conversions
            FROM marketing_campaigns
            GROUP BY campaign_id, campaign_name, marketing_channel
            ORDER BY net_profit DESC
            LIMIT 5;
        """,
        "Query 4: Campaign Performance Tiers by ROAS": """
            SELECT
                campaign_id,
                campaign_name,
                marketing_channel,
                ROUND(SUM(marketing_spend), 2) AS total_spend,
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(((SUM(revenue) - SUM(marketing_spend)) / SUM(marketing_spend)) * 100.0, 2) AS roi_pct,
                ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS roas,
                CASE
                    WHEN SUM(revenue) / SUM(marketing_spend) >= 15.0 THEN 'Elite Tier (ROAS >= 15x)'
                    WHEN SUM(revenue) / SUM(marketing_spend) >= 8.0  THEN 'Strong Performer (8x - 15x)'
                    WHEN SUM(revenue) / SUM(marketing_spend) >= 3.0  THEN 'Moderate Performer (3x - 8x)'
                    WHEN SUM(revenue) / SUM(marketing_spend) >= 1.0  THEN 'Break-Even (1x - 3x)'
                    ELSE 'Loss-Making (< 1x)'
                END AS performance_tier
            FROM marketing_campaigns
            GROUP BY campaign_id, campaign_name, marketing_channel
            ORDER BY roas DESC
            LIMIT 10;
        """,
        "Query 5: Conversion Rates, CTR, and Funnel Rates by Channel": """
            SELECT
                marketing_channel,
                SUM(impressions) AS total_impressions,
                SUM(clicks) AS total_clicks,
                SUM(leads) AS total_leads,
                SUM(conversions) AS total_conversions,
                ROUND((SUM(clicks) * 100.0) / SUM(impressions), 2) AS ctr_pct,
                ROUND((SUM(leads) * 100.0) / SUM(clicks), 2) AS click_to_lead_pct,
                ROUND((SUM(conversions) * 100.0) / SUM(clicks), 2) AS conv_rate_pct,
                ROUND((SUM(conversions) * 100.0) / SUM(leads), 2) AS lead_to_conv_pct
            FROM marketing_campaigns
            GROUP BY marketing_channel
            ORDER BY conv_rate_pct DESC;
        """,
        "Query 6: Underperforming Campaigns (High Spend, Low ROAS)": """
            WITH AvgMetrics AS (
                SELECT
                    AVG(camp_spend) AS avg_spend,
                    AVG(camp_roas) AS avg_roas
                FROM (
                    SELECT
                        campaign_id,
                        SUM(marketing_spend) AS camp_spend,
                        SUM(revenue) / SUM(marketing_spend) AS camp_roas
                    FROM marketing_campaigns
                    GROUP BY campaign_id
                )
            )
            SELECT
                c.campaign_id,
                c.campaign_name,
                c.marketing_channel,
                ROUND(SUM(c.marketing_spend), 2) AS total_spend,
                ROUND(SUM(c.revenue), 2) AS total_revenue,
                ROUND(SUM(c.revenue) - SUM(c.marketing_spend), 2) AS net_profit,
                ROUND(SUM(c.revenue) / SUM(c.marketing_spend), 2) AS roas,
                ROUND(SUM(c.marketing_spend) / SUM(c.conversions), 2) AS cac
            FROM marketing_campaigns c
            CROSS JOIN AvgMetrics a
            GROUP BY c.campaign_id, c.campaign_name, c.marketing_channel, a.avg_spend, a.avg_roas
            HAVING SUM(c.marketing_spend) >= a.avg_spend * 0.90
               AND (SUM(c.revenue) / SUM(c.marketing_spend)) < a.avg_roas
            ORDER BY roas ASC
            LIMIT 10;
        """,
        "Query 7: Monthly Revenue Growth and Trends (MoM with LAG)": """
            WITH MonthlyMetrics AS (
                SELECT
                    year,
                    month,
                    month_name,
                    month_year,
                    ROUND(SUM(marketing_spend), 2) AS monthly_spend,
                    ROUND(SUM(revenue), 2) AS monthly_revenue,
                    ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS monthly_profit,
                    SUM(conversions) AS monthly_conversions
                FROM marketing_campaigns
                GROUP BY year, month, month_name, month_year
            )
            SELECT
                month_year,
                monthly_spend,
                monthly_revenue,
                monthly_profit,
                LAG(monthly_revenue, 1) OVER (ORDER BY year, month) AS prior_month_revenue,
                ROUND(monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month), 2) AS mom_change_usd,
                ROUND(
                    ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month))
                     / LAG(monthly_revenue, 1) OVER (ORDER BY year, month)) * 100.0,
                    2
                ) AS mom_growth_pct,
                ROUND(monthly_revenue / monthly_spend, 2) AS monthly_roas
            FROM MonthlyMetrics
            ORDER BY year, month;
        """,
        "Query 8: Most Effective Marketing Channel (Composite Scoring)": """
            WITH ChannelStats AS (
                SELECT
                    marketing_channel,
                    ROUND(SUM(marketing_spend), 2) AS spend,
                    ROUND(SUM(revenue), 2) AS revenue,
                    ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS roas,
                    ROUND(SUM(marketing_spend) / SUM(conversions), 2) AS cac,
                    ROUND((SUM(conversions) * 100.0) / SUM(clicks), 2) AS conv_rate,
                    SUM(conversions) AS total_conversions
                FROM marketing_campaigns
                GROUP BY marketing_channel
            ),
            RankedChannels AS (
                SELECT
                    marketing_channel,
                    spend,
                    revenue,
                    roas,
                    cac,
                    conv_rate,
                    total_conversions,
                    DENSE_RANK() OVER (ORDER BY roas DESC) AS roas_rank,
                    DENSE_RANK() OVER (ORDER BY cac ASC) AS cac_rank,
                    DENSE_RANK() OVER (ORDER BY conv_rate DESC) AS conv_rate_rank
                FROM ChannelStats
            )
            SELECT
                marketing_channel,
                spend,
                revenue,
                roas,
                cac,
                conv_rate,
                total_conversions,
                roas_rank,
                cac_rank,
                conv_rate_rank,
                (roas_rank + cac_rank + conv_rate_rank) AS composite_rank_sum,
                DENSE_RANK() OVER (ORDER BY (roas_rank + cac_rank + conv_rate_rank) ASC) AS overall_rank
            FROM RankedChannels
            ORDER BY overall_rank ASC;
        """,
        "Query 9: Customer Acquisition Costs (CAC) by Channel & Status": """
            SELECT
                marketing_channel,
                campaign_status,
                COUNT(DISTINCT campaign_id) AS campaign_count,
                ROUND(SUM(marketing_spend), 2) AS total_spend,
                SUM(conversions) AS total_conversions,
                ROUND(SUM(marketing_spend) / SUM(conversions), 2) AS avg_cac,
                ROUND(SUM(marketing_spend) / SUM(clicks), 2) AS avg_cpc,
                ROUND(SUM(marketing_spend) / SUM(leads), 2) AS avg_cpl,
                ROUND(SUM(revenue) / SUM(conversions), 2) AS avg_rev_per_customer
            FROM marketing_campaigns
            GROUP BY marketing_channel, campaign_status
            ORDER BY marketing_channel, avg_cac ASC;
        """,
        "Query 10: Campaign ROAS Leaderboard (DENSE_RANK Window Function)": """
            WITH CampaignROAS AS (
                SELECT
                    campaign_id,
                    campaign_name,
                    marketing_channel,
                    campaign_status,
                    ROUND(SUM(marketing_spend), 2) AS total_spend,
                    ROUND(SUM(revenue), 2) AS total_revenue,
                    ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS net_profit,
                    ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS roas,
                    SUM(conversions) AS conversions
                FROM marketing_campaigns
                GROUP BY campaign_id, campaign_name, marketing_channel, campaign_status
            )
            SELECT
                DENSE_RANK() OVER (ORDER BY roas DESC) AS roas_rank,
                campaign_id,
                campaign_name,
                marketing_channel,
                campaign_status,
                total_spend,
                total_revenue,
                net_profit,
                roas,
                conversions
            FROM CampaignROAS
            ORDER BY roas_rank ASC
            LIMIT 10;
        """,
        "Query 11 (Attribution): First-Touch vs. Last-Touch Channel Conversion & Revenue Shift": """
            WITH FirstTouch AS (
                SELECT
                    customer_id,
                    marketing_channel AS first_channel
                FROM (
                    SELECT
                        customer_id,
                        marketing_channel,
                        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY touchpoint_sequence ASC) AS rn
                    FROM customer_attribution_touchpoints
                    WHERE journey_converted = 1
                )
                WHERE rn = 1
            ),
            LastTouch AS (
                SELECT
                    customer_id,
                    marketing_channel AS last_channel
                FROM (
                    SELECT
                        customer_id,
                        marketing_channel,
                        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY touchpoint_sequence DESC) AS rn
                    FROM customer_attribution_touchpoints
                    WHERE journey_converted = 1
                )
                WHERE rn = 1
            ),
            JourneyRev AS (
                SELECT
                    customer_id,
                    MAX(total_journey_revenue) AS revenue
                FROM customer_attribution_touchpoints
                WHERE journey_converted = 1
                GROUP BY customer_id
            ),
            JoinedData AS (
                SELECT
                    ft.customer_id,
                    ft.first_channel,
                    lt.last_channel,
                    jr.revenue
                FROM FirstTouch ft
                JOIN LastTouch lt ON ft.customer_id = lt.customer_id
                JOIN JourneyRev jr ON ft.customer_id = jr.customer_id
            )
            SELECT
                ft_summary.channel,
                ft_summary.first_touch_conversions,
                ft_summary.first_touch_revenue,
                lt_summary.last_touch_conversions,
                lt_summary.last_touch_revenue,
                ROUND(lt_summary.last_touch_revenue - ft_summary.first_touch_revenue, 2) AS revenue_shift_last_minus_first
            FROM (
                SELECT first_channel AS channel, COUNT(*) AS first_touch_conversions, ROUND(SUM(revenue), 2) AS first_touch_revenue
                FROM JoinedData
                GROUP BY first_channel
            ) ft_summary
            JOIN (
                SELECT last_channel AS channel, COUNT(*) AS last_touch_conversions, ROUND(SUM(revenue), 2) AS last_touch_revenue
                FROM JoinedData
                GROUP BY last_channel
            ) lt_summary ON ft_summary.channel = lt_summary.channel
            ORDER BY ft_summary.first_touch_revenue DESC;
        """
    }

    md_report = []
    md_report.append("# Marketing Attribution and ROI Intelligence: SQL Analytical Query Results\n")
    md_report.append("This document contains verified query outputs executed on the complete marketing dataset.\n")

    for title, q in queries.items():
        print(f"Executing: {title}...")
        df_res = pd.read_sql_query(q, conn)
        
        md_report.append(f"## {title}\n")
        md_report.append("```sql")
        md_report.append(q.strip())
        md_report.append("```\n")
        md_report.append("### Query Output Table\n")
        md_report.append(df_to_markdown(df_res))
        md_report.append("\n---\n")

    output_path = "reports/sql_query_results.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_report))
    print(f"\nAll SQL queries successfully executed and results exported to: {output_path}")

    conn.close()


if __name__ == "__main__":
    run_all_sql_queries()
