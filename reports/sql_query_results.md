# Marketing Attribution and ROI Intelligence: SQL Analytical Query Results

This document contains verified query outputs executed on the complete marketing dataset.

## Query 1: Total Marketing Expenditure, Revenue, Profit & Portfolio ROI

```sql
SELECT
                COUNT(*) AS total_campaign_records,
                ROUND(SUM(marketing_spend), 2) AS total_marketing_expenditure,
                ROUND(SUM(revenue), 2) AS total_revenue_generated,
                ROUND(SUM(revenue) - SUM(marketing_spend), 2) AS total_net_profit,
                ROUND(((SUM(revenue) - SUM(marketing_spend)) / SUM(marketing_spend)) * 100.0, 2) AS overall_roi_percentage,
                ROUND(SUM(revenue) / SUM(marketing_spend), 2) AS overall_portfolio_roas
            FROM marketing_campaigns;
```

### Query Output Table

| total_campaign_records | total_marketing_expenditure | total_revenue_generated | total_net_profit | overall_roi_percentage | overall_portfolio_roas |
| --- | --- | --- | --- | --- | --- |
| 8572.0 | 4678276.51 | 52091563.43 | 47413286.92 | 1013.48 | 11.13 |

---

## Query 2: Total Revenue, Spend, Profit, and ROAS by Marketing Channel

```sql
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
```

### Query Output Table

| marketing_channel | active_campaigns_count | total_spend | total_revenue | net_profit | channel_roi_pct | channel_roas | pct_of_total_revenue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Organic Search | 6 | 422825.41 | 20858828.91 | 20436003.5 | 4833.2 | 49.33 | 40.04 |
| Email Marketing | 6 | 268273.4 | 12105908.49 | 11837635.09 | 4412.53 | 45.13 | 23.24 |
| Referral Marketing | 6 | 582772.19 | 8295055.41 | 7712283.22 | 1323.38 | 14.23 | 15.92 |
| Google Ads | 6 | 1397654.59 | 4761599.72 | 3363945.13 | 240.69 | 3.41 | 9.14 |
| Facebook Ads | 6 | 1099135.87 | 3620927.28 | 2521791.41 | 229.43 | 3.29 | 6.95 |
| Instagram Ads | 6 | 907615.05 | 2449243.62 | 1541628.57 | 169.85 | 2.7 | 4.7 |

---

## Query 3: Top 5 Profitable Campaigns

```sql
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
```

### Query Output Table

| campaign_id | campaign_name | marketing_channel | total_spend | total_revenue | net_profit | roi_pct | roas | total_conversions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP-125 | Organic_Search_SEO_Comprehensive_Buying_Guides | Organic Search | 77246.79 | 4069934.02 | 3992687.23 | 5168.74 | 52.69 | 23301 |
| CMP-126 | Organic_Search_SEO_Category_Hub_Pages | Organic Search | 74274.45 | 3635913.36 | 3561638.91 | 4795.24 | 48.95 | 20875 |
| CMP-130 | Organic_Search_SEO_Top_10_Reviews | Organic Search | 67311.53 | 3412501.2 | 3345189.67 | 4969.71 | 50.7 | 19636 |
| CMP-128 | Organic_Search_SEO_Technical_Optimization | Organic Search | 70607.22 | 3353523.39 | 3282916.17 | 4649.55 | 47.5 | 19934 |
| CMP-129 | Organic_Search_SEO_How_To_Tutorials | Organic Search | 67570.37 | 3252971.62 | 3185401.25 | 4714.2 | 48.14 | 18959 |

---

## Query 4: Campaign Performance Tiers by ROAS

```sql
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
```

### Query Output Table

| campaign_id | campaign_name | marketing_channel | total_spend | total_revenue | roi_pct | roas | performance_tier |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMP-125 | Organic_Search_SEO_Comprehensive_Buying_Guides | Organic Search | 77246.79 | 4069934.02 | 5168.74 | 52.69 | Elite Tier (ROAS >= 15x) |
| CMP-130 | Organic_Search_SEO_Top_10_Reviews | Organic Search | 67311.53 | 3412501.2 | 4969.71 | 50.7 | Elite Tier (ROAS >= 15x) |
| CMP-126 | Organic_Search_SEO_Category_Hub_Pages | Organic Search | 74274.45 | 3635913.36 | 4795.24 | 48.95 | Elite Tier (ROAS >= 15x) |
| CMP-129 | Organic_Search_SEO_How_To_Tutorials | Organic Search | 67570.37 | 3252971.62 | 4714.2 | 48.14 | Elite Tier (ROAS >= 15x) |
| CMP-124 | Email_Marketing_Seasonal_Flash_Sale | Email Marketing | 49939.88 | 2393646.92 | 4693.06 | 47.93 | Elite Tier (ROAS >= 15x) |
| CMP-127 | Organic_Search_SEO_Product_Comparison_Articles | Organic Search | 65815.05 | 3133985.32 | 4661.81 | 47.62 | Elite Tier (ROAS >= 15x) |
| CMP-128 | Organic_Search_SEO_Technical_Optimization | Organic Search | 70607.22 | 3353523.39 | 4649.55 | 47.5 | Elite Tier (ROAS >= 15x) |
| CMP-121 | Email_Marketing_VIP_Loyalty_Exclusive | Email Marketing | 41872.7 | 1946896.13 | 4549.56 | 46.5 | Elite Tier (ROAS >= 15x) |
| CMP-119 | Email_Marketing_Welcome_Series_Drip | Email Marketing | 44344.8 | 1983792.02 | 4373.56 | 44.74 | Elite Tier (ROAS >= 15x) |
| CMP-122 | Email_Marketing_Weekly_Newsletter_Curated | Email Marketing | 42609.23 | 1904037.62 | 4368.6 | 44.69 | Elite Tier (ROAS >= 15x) |

---

## Query 5: Conversion Rates, CTR, and Funnel Rates by Channel

```sql
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
```

### Query Output Table

| marketing_channel | total_impressions | total_clicks | total_leads | total_conversions | ctr_pct | click_to_lead_pct | conv_rate_pct | lead_to_conv_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Email Marketing | 18415858 | 908952 | 198161 | 74937 | 4.94 | 21.8 | 8.24 | 37.82 |
| Referral Marketing | 15526266 | 619699 | 123371 | 43323 | 3.99 | 19.91 | 6.99 | 35.12 |
| Organic Search | 44917723 | 1937078 | 350432 | 121111 | 4.31 | 18.09 | 6.25 | 34.56 |
| Google Ads | 12956736 | 471334 | 65360 | 25798 | 3.64 | 13.87 | 5.47 | 39.47 |
| Facebook Ads | 32854602 | 753669 | 75766 | 26077 | 2.29 | 10.05 | 3.46 | 34.42 |
| Instagram Ads | 41091734 | 707217 | 56367 | 19868 | 1.72 | 7.97 | 2.81 | 35.25 |

---

## Query 6: Underperforming Campaigns (High Spend, Low ROAS)

```sql
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
```

### Query Output Table

| campaign_id | campaign_name | marketing_channel | total_spend | total_revenue | net_profit | roas | cac |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMP-114 | Instagram_Ads_Reels_Product_Showcase | Instagram Ads | 153333.98 | 398215.95 | 244881.97 | 2.6 | 47.89 |
| CMP-116 | Instagram_Ads_Feed_Visual_Storytelling | Instagram Ads | 142358.41 | 377784.79 | 235426.38 | 2.65 | 45.57 |
| CMP-118 | Instagram_Ads_Holiday_Special_Stories | Instagram Ads | 160188.3 | 428412.43 | 268224.13 | 2.67 | 46.65 |
| CMP-117 | Instagram_Ads_Retargeting_Product_Carousel | Instagram Ads | 144731.57 | 391497.0 | 246765.43 | 2.7 | 45.98 |
| CMP-113 | Instagram_Ads_Stories_Influencer_Collab | Instagram Ads | 163047.08 | 447492.93 | 284445.85 | 2.74 | 44.66 |
| CMP-115 | Instagram_Ads_Explore_Awareness_Campaign | Instagram Ads | 143955.71 | 405840.52 | 261884.81 | 2.82 | 43.5 |
| CMP-108 | Facebook_Ads_Feed_Prospecting_Interests | Facebook Ads | 178772.49 | 560807.18 | 382034.69 | 3.14 | 42.34 |
| CMP-107 | Facebook_Ads_Feed_Lookalike_Audience_1pct | Facebook Ads | 195954.91 | 629488.42 | 433533.51 | 3.21 | 43.14 |
| CMP-111 | Facebook_Ads_Catalog_Dynamic_Product_Ads | Facebook Ads | 156175.75 | 501926.56 | 345750.81 | 3.21 | 43.35 |
| CMP-103 | Google_Ads_Search_Competitor_Conquesting | Google Ads | 253531.9 | 830444.46 | 576912.56 | 3.28 | 55.42 |

---

## Query 7: Monthly Revenue Growth and Trends (MoM with LAG)

```sql
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
```

### Query Output Table

| month_year | monthly_spend | monthly_revenue | monthly_profit | prior_month_revenue | mom_change_usd | mom_growth_pct | monthly_roas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-01 | 329020.53 | 3550200.12 | 3221179.59 | nan | nan | nan | 10.79 |
| 2025-02 | 305902.45 | 3196555.32 | 2890652.87 | 3550200.12 | -353644.8 | -9.96 | 10.45 |
| 2025-03 | 414105.48 | 4270984.66 | 3856879.19 | 3196555.32 | 1074429.34 | 33.61 | 10.31 |
| 2025-04 | 388486.08 | 4122179.99 | 3733693.91 | 4270984.66 | -148804.67 | -3.48 | 10.61 |
| 2025-05 | 358312.21 | 3827447.57 | 3469135.36 | 4122179.99 | -294732.42 | -7.15 | 10.68 |
| 2025-06 | 356751.09 | 4180290.5 | 3823539.41 | 3827447.57 | 352842.93 | 9.22 | 11.72 |
| 2025-07 | 425585.99 | 5374561.69 | 4948975.7 | 4180290.5 | 1194271.19 | 28.57 | 12.63 |
| 2025-08 | 378339.83 | 4421062.08 | 4042722.25 | 5374561.69 | -953499.61 | -17.74 | 11.69 |
| 2025-09 | 366381.24 | 3602206.55 | 3235825.31 | 4421062.08 | -818855.53 | -18.52 | 9.83 |
| 2025-10 | 359371.21 | 3808331.77 | 3448960.56 | 3602206.55 | 206125.22 | 5.72 | 10.6 |
| 2025-11 | 488386.3 | 5592922.81 | 5104536.52 | 3808331.77 | 1784591.04 | 46.86 | 11.45 |
| 2025-12 | 507634.1 | 6144820.37 | 5637186.27 | 5592922.81 | 551897.56 | 9.87 | 12.1 |

---

## Query 8: Most Effective Marketing Channel (Composite Scoring)

```sql
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
```

### Query Output Table

| marketing_channel | spend | revenue | roas | cac | conv_rate | total_conversions | roas_rank | cac_rank | conv_rate_rank | composite_rank_sum | overall_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Organic Search | 422825.41 | 20858828.91 | 49.33 | 3.49 | 6.25 | 121111 | 1 | 1 | 3 | 5 | 1 |
| Email Marketing | 268273.4 | 12105908.49 | 45.13 | 3.58 | 8.24 | 74937 | 2 | 2 | 1 | 5 | 1 |
| Referral Marketing | 582772.19 | 8295055.41 | 14.23 | 13.45 | 6.99 | 43323 | 3 | 3 | 2 | 8 | 2 |
| Google Ads | 1397654.59 | 4761599.72 | 3.41 | 54.18 | 5.47 | 25798 | 4 | 6 | 4 | 14 | 3 |
| Facebook Ads | 1099135.87 | 3620927.28 | 3.29 | 42.15 | 3.46 | 26077 | 5 | 4 | 5 | 14 | 3 |
| Instagram Ads | 907615.05 | 2449243.62 | 2.7 | 45.68 | 2.81 | 19868 | 6 | 5 | 6 | 17 | 4 |

---

## Query 9: Customer Acquisition Costs (CAC) by Channel & Status

```sql
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
```

### Query Output Table

| marketing_channel | campaign_status | campaign_count | total_spend | total_conversions | avg_cac | avg_cpc | avg_cpl | avg_rev_per_customer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Email Marketing | Active | 6 | 218943.14 | 61284 | 3.57 | 0.29 | 1.35 | 161.01 |
| Email Marketing | Completed | 6 | 36639.65 | 10136 | 3.61 | 0.3 | 1.38 | 162.69 |
| Email Marketing | Paused | 6 | 12690.61 | 3517 | 3.61 | 0.3 | 1.41 | 167.62 |
| Facebook Ads | Completed | 6 | 286156.48 | 6897 | 41.49 | 1.44 | 14.37 | 137.33 |
| Facebook Ads | Paused | 6 | 110807.31 | 2641 | 41.96 | 1.44 | 14.48 | 141.48 |
| Facebook Ads | Active | 6 | 702172.08 | 16539 | 42.46 | 1.47 | 14.57 | 139.07 |
| Google Ads | Completed | 6 | 270367.61 | 5270 | 51.3 | 2.83 | 20.79 | 182.95 |
| Google Ads | Active | 6 | 997713.87 | 18172 | 54.9 | 3.01 | 21.56 | 184.29 |
| Google Ads | Paused | 6 | 129573.11 | 2356 | 55.0 | 2.93 | 21.33 | 190.36 |
| Instagram Ads | Completed | 6 | 226262.19 | 5081 | 44.53 | 1.28 | 16.35 | 121.41 |
| Instagram Ads | Paused | 6 | 82391.11 | 1811 | 45.49 | 1.3 | 15.47 | 122.01 |
| Instagram Ads | Active | 6 | 598961.75 | 12976 | 46.16 | 1.28 | 16.1 | 124.18 |
| Organic Search | Paused | 6 | 18241.89 | 5474 | 3.33 | 0.21 | 1.19 | 159.0 |
| Organic Search | Completed | 6 | 40017.22 | 11994 | 3.34 | 0.21 | 1.16 | 169.74 |
| Organic Search | Active | 6 | 364566.3 | 103643 | 3.52 | 0.22 | 1.21 | 173.22 |
| Referral Marketing | Paused | 6 | 58000.33 | 4519 | 12.83 | 0.9 | 4.51 | 190.39 |
| Referral Marketing | Active | 6 | 439670.99 | 32724 | 13.44 | 0.94 | 4.74 | 192.11 |
| Referral Marketing | Completed | 6 | 85100.87 | 6080 | 14.0 | 0.96 | 4.8 | 188.81 |

---

## Query 10: Campaign ROAS Leaderboard (DENSE_RANK Window Function)

```sql
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
```

### Query Output Table

| roas_rank | campaign_id | campaign_name | marketing_channel | campaign_status | total_spend | total_revenue | net_profit | roas | conversions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CMP-125 | Organic_Search_SEO_Comprehensive_Buying_Guides | Organic Search | Completed | 7653.19 | 477087.3 | 469434.11 | 62.34 | 2806 |
| 2 | CMP-126 | Organic_Search_SEO_Category_Hub_Pages | Organic Search | Paused | 2933.11 | 162914.63 | 159981.52 | 55.54 | 1105 |
| 3 | CMP-124 | Email_Marketing_Seasonal_Flash_Sale | Email Marketing | Paused | 2159.28 | 119653.09 | 117493.81 | 55.41 | 668 |
| 4 | CMP-125 | Organic_Search_SEO_Comprehensive_Buying_Guides | Organic Search | Paused | 3611.63 | 193888.7 | 190277.07 | 53.68 | 1166 |
| 5 | CMP-128 | Organic_Search_SEO_Technical_Optimization | Organic Search | Completed | 6606.97 | 354454.36 | 347847.39 | 53.65 | 2059 |
| 6 | CMP-129 | Organic_Search_SEO_How_To_Tutorials | Organic Search | Completed | 5898.74 | 313278.22 | 307379.48 | 53.11 | 1877 |
| 7 | CMP-121 | Email_Marketing_VIP_Loyalty_Exclusive | Email Marketing | Completed | 3746.67 | 194357.15 | 190610.48 | 51.87 | 1162 |
| 8 | CMP-130 | Organic_Search_SEO_Top_10_Reviews | Organic Search | Active | 57819.18 | 2991689.87 | 2933870.69 | 51.74 | 17199 |
| 9 | CMP-125 | Organic_Search_SEO_Comprehensive_Buying_Guides | Organic Search | Active | 65981.97 | 3398958.02 | 3332976.05 | 51.51 | 19329 |
| 10 | CMP-120 | Email_Marketing_Cart_Abandonment_Sequence | Email Marketing | Paused | 1951.64 | 100222.3 | 98270.66 | 51.35 | 525 |

---

## Query 11 (Attribution): First-Touch vs. Last-Touch Channel Conversion & Revenue Shift

```sql
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
```

### Query Output Table

| channel | first_touch_conversions | first_touch_revenue | last_touch_conversions | last_touch_revenue | revenue_shift_last_minus_first |
| --- | --- | --- | --- | --- | --- |
| Organic Search | 1064 | 200513.91 | 554 | 105047.43 | -95466.48 |
| Facebook Ads | 821 | 156524.3 | 369 | 70064.5 | -86459.8 |
| Instagram Ads | 595 | 114734.24 | 302 | 57273.26 | -57460.98 |
| Google Ads | 299 | 55178.02 | 992 | 188893.83 | 133715.81 |
| Email Marketing | 82 | 15570.99 | 448 | 85528.75 | 69957.76 |
| Referral Marketing | 65 | 12750.81 | 261 | 48464.5 | 35713.69 |

---
