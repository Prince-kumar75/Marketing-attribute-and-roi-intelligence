-- ==============================================================================
-- Marketing Attribution and ROI Intelligence
-- Production Business Analytics SQL Queries
-- PostgreSQL / MySQL / SQLite ANSI SQL Compatible
-- ==============================================================================

-- ==============================================================================
-- QUERY 1: Calculate Total Marketing Expenditure, Revenue, Profit, and Blended ROI
-- Business Goal: High-level financial audit of marketing capital deployment.
-- ==============================================================================
SELECT
    COUNT(*) AS total_campaign_records,
    ROUND(SUM(marketing_spend), 2) AS total_marketing_expenditure,
    ROUND(SUM(revenue), 2) AS total_revenue_generated,
    ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS total_net_profit,
    ROUND(((SUM(revenue) - SUM(marketing_spend)) / NULLIF(SUM(marketing_spend), 0)) * 100, 2) AS overall_roi_percentage,
    ROUND(SUM(revenue) / NULLIF(SUM(marketing_spend), 0), 2) AS overall_portfolio_roas
FROM marketing_campaigns;


-- ==============================================================================
-- QUERY 2: Calculate Total Revenue, Spend, Profit, and ROAS by Marketing Channel
-- Business Goal: Identify top revenue contributing channels across the portfolio.
-- ==============================================================================
SELECT
    marketing_channel,
    COUNT(DISTINCT campaign_id) AS active_campaigns_count,
    ROUND(SUM(marketing_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS net_profit,
    ROUND(((SUM(revenue) - SUM(marketing_spend)) / NULLIF(SUM(marketing_spend), 0)) * 100, 2) AS channel_roi_pct,
    ROUND(SUM(revenue) / NULLIF(SUM(marketing_spend), 0), 2) AS channel_roas,
    ROUND(100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS pct_of_total_revenue
FROM marketing_campaigns
GROUP BY marketing_channel
ORDER BY total_revenue DESC;


-- ==============================================================================
-- QUERY 3: Identify the Top 5 Most Profitable Campaigns
-- Business Goal: Pinpoint elite campaigns generating the greatest net dollar profit.
-- ==============================================================================
SELECT
    campaign_id,
    campaign_name,
    marketing_channel,
    ROUND(SUM(marketing_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS net_profit,
    ROUND(((SUM(revenue) - SUM(marketing_spend)) / NULLIF(SUM(marketing_spend), 0)) * 100, 2) AS roi_percentage,
    ROUND(SUM(revenue) / NULLIF(SUM(marketing_spend), 0), 2) AS roas_multiple,
    SUM(conversions) AS total_conversions
FROM marketing_campaigns
GROUP BY campaign_id, campaign_name, marketing_channel
ORDER BY net_profit DESC
LIMIT 5;


-- ==============================================================================
-- QUERY 4: Calculate Return on Investment (ROI) for Each Campaign
-- Business Goal: Audit campaign capital efficiency and categorize performance tiers.
-- Uses: CASE WHEN tiering logic
-- ==============================================================================
SELECT
    campaign_id,
    campaign_name,
    marketing_channel,
    ROUND(SUM(marketing_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(((SUM(revenue) - SUM(marketing_spend)) / NULLIF(SUM(marketing_spend), 0)) * 100, 2) AS campaign_roi_pct,
    ROUND(SUM(revenue) / NULLIF(SUM(marketing_spend), 0), 2) AS campaign_roas,
    CASE
        WHEN SUM(revenue) / NULLIF(SUM(marketing_spend), 0) >= 15.0 THEN 'Elite Tier (ROAS >= 15x)'
        WHEN SUM(revenue) / NULLIF(SUM(marketing_spend), 0) >= 8.0  THEN 'Strong Performer (8x - 15x)'
        WHEN SUM(revenue) / NULLIF(SUM(marketing_spend), 0) >= 3.0  THEN 'Moderate Performer (3x - 8x)'
        WHEN SUM(revenue) / NULLIF(SUM(marketing_spend), 0) >= 1.0  THEN 'Break-Even (1x - 3x)'
        ELSE 'Loss-Making (< 1x)'
    END AS performance_tier
FROM marketing_campaigns
GROUP BY campaign_id, campaign_name, marketing_channel
ORDER BY campaign_roi_pct DESC;


-- ==============================================================================
-- QUERY 5: Calculate Conversion Rates, CTR, and Funnel Drop-off by Channel
-- Business Goal: Measure visitor engagement and click-to-customer conversion efficiency.
-- ==============================================================================
SELECT
    marketing_channel,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(leads) AS total_leads,
    SUM(conversions) AS total_conversions,
    ROUND((SUM(clicks) * 100.0) / NULLIF(SUM(impressions), 0), 2) AS ctr_pct,
    ROUND((SUM(leads) * 100.0) / NULLIF(SUM(clicks), 0), 2) AS click_to_lead_rate_pct,
    ROUND((SUM(conversions) * 100.0) / NULLIF(SUM(clicks), 0), 2) AS conversion_rate_pct,
    ROUND((SUM(conversions) * 100.0) / NULLIF(SUM(leads), 0), 2) AS lead_to_conversion_rate_pct
FROM marketing_campaigns
GROUP BY marketing_channel
ORDER BY conversion_rate_pct DESC;


-- ==============================================================================
-- QUERY 6: Identify Campaigns with High Spend and Low Revenue (Budget Bleeders)
-- Business Goal: Detect underperforming campaigns with spend above average but ROAS < 4.0x.
-- Uses: CTEs, Subqueries, HAVING
-- ==============================================================================
WITH CampaignAverages AS (
    SELECT
        AVG(campaign_spend) AS avg_spend,
        AVG(campaign_roas) AS avg_roas
    FROM (
        SELECT
            campaign_id,
            SUM(marketing_spend) AS campaign_spend,
            SUM(revenue) / NULLIF(SUM(marketing_spend), 0) AS campaign_roas
        FROM marketing_campaigns
        GROUP BY campaign_id
    ) sub
)
SELECT
    c.campaign_id,
    c.campaign_name,
    c.marketing_channel,
    ROUND(SUM(c.marketing_spend), 2) AS total_spend,
    ROUND(SUM(c.revenue), 2) AS total_revenue,
    ROUND(SUM(c.revenue) - SUM(c.marketing_spend), 2) AS net_profit,
    ROUND(SUM(c.revenue) / NULLIF(SUM(c.marketing_spend), 0), 2) AS roas,
    ROUND(SUM(c.marketing_spend) / NULLIF(SUM(c.conversions), 0), 2) AS cac
FROM marketing_campaigns c
CROSS JOIN CampaignAverages ca
GROUP BY c.campaign_id, c.campaign_name, c.marketing_channel, ca.avg_spend, ca.avg_roas
HAVING SUM(c.marketing_spend) >= ca.avg_spend * 0.90
   AND (SUM(c.revenue) / NULLIF(SUM(c.marketing_spend), 0)) < ca.avg_roas
ORDER BY roas ASC
LIMIT 10;


-- ==============================================================================
-- QUERY 7: Calculate Monthly Revenue Growth (Month-over-Month MoM)
-- Business Goal: Measure revenue momentum and seasonal expansion/contraction.
-- Uses: Window Function LAG() OVER (ORDER BY ...)
-- ==============================================================================
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
    year,
    month,
    month_name,
    month_year,
    monthly_spend,
    monthly_revenue,
    monthly_profit,
    LAG(monthly_revenue, 1) OVER (ORDER BY year, month) AS prior_month_revenue,
    ROUND(monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month), 2) AS mom_revenue_change_usd,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month))
         / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY year, month), 0)) * 100.0,
        2
    ) AS mom_revenue_growth_pct,
    ROUND(monthly_revenue / NULLIF(monthly_spend, 0), 2) AS monthly_roas
FROM MonthlyMetrics
ORDER BY year, month;


-- ==============================================================================
-- QUERY 8: Find the Most Effective Marketing Channel (Composite Scoring)
-- Business Goal: Rank channels using a composite weighted score of ROAS, CAC, and Conv Rate.
-- Uses: Window ranking functions and normalized scoring CTEs
-- ==============================================================================
WITH ChannelStats AS (
    SELECT
        marketing_channel,
        ROUND(SUM(marketing_spend), 2) AS spend,
        ROUND(SUM(revenue), 2) AS revenue,
        ROUND(SUM(revenue) / NULLIF(SUM(marketing_spend), 0), 2) AS roas,
        ROUND(SUM(marketing_spend) / NULLIF(SUM(conversions), 0), 2) AS cac,
        ROUND((SUM(conversions) * 100.0) / NULLIF(SUM(clicks), 0), 2) AS conv_rate,
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
    DENSE_RANK() OVER (ORDER BY (roas_rank + cac_rank + conv_rate_rank) ASC) AS overall_effectiveness_rank
FROM RankedChannels
ORDER BY overall_effectiveness_rank ASC;


-- ==============================================================================
-- QUERY 9: Analyze Customer Acquisition Costs (CAC) across Channels & Campaign Status
-- Business Goal: Compare cost efficiency of acquiring paying customers across operational states.
-- ==============================================================================
SELECT
    marketing_channel,
    campaign_status,
    COUNT(DISTINCT campaign_id) AS campaign_count,
    ROUND(SUM(marketing_spend), 2) AS total_spend,
    SUM(conversions) AS total_conversions,
    ROUND(SUM(marketing_spend) / NULLIF(SUM(conversions), 0), 2) AS avg_cac,
    ROUND(SUM(marketing_spend) / NULLIF(SUM(clicks), 0), 2) AS avg_cpc,
    ROUND(SUM(marketing_spend) / NULLIF(SUM(leads), 0), 2) AS avg_cpl,
    ROUND(SUM(revenue) / NULLIF(SUM(conversions), 0), 2) AS avg_revenue_per_customer,
    ROUND(
        (SUM(revenue) / NULLIF(SUM(conversions), 0)) -
        (SUM(marketing_spend) / NULLIF(SUM(conversions), 0)),
        2
    ) AS net_margin_per_customer
FROM marketing_campaigns
GROUP BY marketing_channel, campaign_status
ORDER BY marketing_channel, avg_cac ASC;


-- ==============================================================================
-- QUERY 10: Rank All Campaigns Based on Return on Advertising Spend (ROAS)
-- Business Goal: Global leaderboard of campaigns using Window DENSE_RANK()
-- Uses: DENSE_RANK() OVER (ORDER BY ROAS DESC), ROW_NUMBER()
-- ==============================================================================
WITH CampaignROAS AS (
    SELECT
        campaign_id,
        campaign_name,
        marketing_channel,
        campaign_status,
        ROUND(SUM(marketing_spend), 2) AS total_spend,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS net_profit,
        ROUND(SUM(revenue) / NULLIF(SUM(marketing_spend), 0), 2) AS roas,
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
ORDER BY roas_rank ASC;


-- ==============================================================================
-- BONUS QUERY 11: SQL Multi-Touch Attribution Engine (First-Touch vs. Last-Touch)
-- Business Goal: Demonstrate pure SQL implementation of attribution modeling
-- Uses: FIRST_VALUE(), LAST_VALUE() Window Functions with Frames
-- ==============================================================================
WITH JourneyTouchpoints AS (
    SELECT
        customer_id,
        marketing_channel,
        touchpoint_sequence,
        total_journey_revenue,
        journey_converted,
        FIRST_VALUE(marketing_channel) OVER (
            PARTITION BY customer_id
            ORDER BY touchpoint_sequence ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_touch_channel,
        LAST_VALUE(marketing_channel) OVER (
            PARTITION BY customer_id
            ORDER BY touchpoint_sequence ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_touch_channel
    FROM customer_attribution_touchpoints
    WHERE journey_converted = 1
),
CustomerLevelAttribution AS (
    SELECT DISTINCT
        customer_id,
        first_touch_channel,
        last_touch_channel,
        total_journey_revenue
    FROM JourneyTouchpoints
)
SELECT
    COALESCE(ft.channel, lt.channel) AS marketing_channel,
    COALESCE(ft.first_touch_conversions, 0) AS first_touch_conversions,
    COALESCE(ft.first_touch_revenue, 0.00) AS first_touch_revenue,
    COALESCE(lt.last_touch_conversions, 0) AS last_touch_conversions,
    COALESCE(lt.last_touch_revenue, 0.00) AS last_touch_revenue,
    ROUND(COALESCE(lt.last_touch_revenue, 0.00) - COALESCE(ft.first_touch_revenue, 0.00), 2) AS revenue_shift_last_minus_first
FROM (
    SELECT
        first_touch_channel AS channel,
        COUNT(*) AS first_touch_conversions,
        ROUND(SUM(total_journey_revenue), 2) AS first_touch_revenue
    FROM CustomerLevelAttribution
    GROUP BY first_touch_channel
) ft
FULL OUTER JOIN (
    SELECT
        last_touch_channel AS channel,
        COUNT(*) AS last_touch_conversions,
        ROUND(SUM(total_journey_revenue), 2) AS last_touch_revenue
    FROM CustomerLevelAttribution
    GROUP BY last_touch_channel
) lt ON ft.channel = lt.channel
ORDER BY first_touch_revenue DESC;
