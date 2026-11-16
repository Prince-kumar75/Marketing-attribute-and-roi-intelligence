# Power BI Interactive Marketing Analytics Dashboard - Implementation Guide

This guide provides step-by-step instructions to replicate the complete 4-Page Enterprise Marketing Attribution and ROI Intelligence Dashboard in **Power BI Desktop**.

---

## 1. Data Source Connection & Ingestion

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Ingest the following processed files:
   - `data/processed/marketing_campaign_data_cleaned.csv` -> Rename query to `Fact_Marketing_Campaigns`
   - `data/processed/marketing_attribution_summary.csv` -> Rename query to `Fact_Attribution_Summary` (Filter out `Total` row)
   - `data/processed/customer_attribution_touchpoints.csv` -> Rename query to `Fact_Attribution_Touchpoints`
4. In **Power Query Editor**:
   - Ensure `Campaign Date` is typed as **Date**.
   - Ensure `Marketing Spend`, `Revenue`, `Net Profit` are **Fixed Decimal Number (Currency)**.
   - Ensure `Impressions`, `Clicks`, `Leads`, `Conversions` are **Whole Number**.
5. Click **Close & Apply**.

---

## 2. Data Modeling & Relationships (Star Schema)

Switch to the **Model View** tab and configure relationships:

- **Dim_Date** `[Date]` (1) <---> (*) `Fact_Marketing_Campaigns` `[Campaign Date]`
- **Dim_Channel** `[Channel_Name]` (1) <---> (*) `Fact_Marketing_Campaigns` `[Marketing Channel]`
- **Dim_Channel** `[Channel_Name]` (1) <---> (1) `Fact_Attribution_Summary` `[Marketing Channel]`
- **Dim_Campaign** `[Campaign_ID]` (1) <---> (*) `Fact_Marketing_Campaigns` `[Campaign ID]`

Set Cross Filter Direction to **Single** (Many to One) except for `Fact_Attribution_Summary` which can be set to **Both**.

---

## 3. Import DAX Measures

1. Open the file `power_bi/dax_measures.dax`.
2. Create a dedicated measure table called `_Measures`.
3. Copy and paste all 30+ measures into the model.

Key core measures to verify:
- `[Total Spend]` = `SUM(marketing_campaigns[marketing_spend])`
- `[Total Revenue]` = `SUM(marketing_campaigns[revenue])`
- `[Net Profit]` = `[Total Revenue] - [Total Spend]`
- `[ROAS]` = `DIVIDE([Total Revenue], [Total Spend], 0)`
- `[ROI %]` = `DIVIDE([Net Profit], [Total Spend], 0)`
- `[CAC]` = `DIVIDE([Total Spend], [Total Conversions], 0)`

---

## 4. Canvas Configuration: 4 Dashboard Pages

### Global Filter Bar (Top Header across all pages)
Add interactive Slicers in a top ribbon:
1. **Date Hierarchy Slicer**: `Campaign Date` (Between slider or Relative Date)
2. **Channel Slicer**: `Marketing Channel` (Dropdown or horizontal pill buttons)
3. **Campaign Status Slicer**: `Campaign Status` (`Active`, `Completed`, `Paused`)
4. **Campaign Search Slicer**: `Campaign Name` (Search text input)

---

### Dashboard Page 1: Executive Overview
**Objective**: Immediate C-Suite visibility into marketing health, capital efficiency, and revenue generation.

- **KPI Card Row (Top)**:
  - Card 1: `[Total Spend]` (Formatted as `$#,##0`)
  - Card 2: `[Total Revenue]` (Formatted as `$#,##0`)
  - Card 3: `[Overall ROI %]` (Formatted as `0.0%`)
  - Card 4: `[ROAS]` (Formatted as `0.00x`)
  - Card 5: `[Total Conversions]` (Formatted as `#,##0`)
  - Card 6: `[Total Leads]` (Formatted as `#,##0`)
- **Visual 1 (Left Area)**: *Line and Clustered Column Chart*
  - Shared Axis: `Month_Name`
  - Column Values: `[Total Spend]`, `[Total Revenue]`
  - Line Values: `[ROAS]`
- **Visual 2 (Right Top)**: *Donut Chart*
  - Legend: `Marketing Channel`
  - Values: `[Total Revenue]`
- **Visual 3 (Bottom Table)**: *Matrix Visual*
  - Rows: `Marketing Channel`
  - Values: `[Total Spend]`, `[Total Revenue]`, `[Net Profit]`, `[ROAS]`, `[ROI %]`, `[CAC]`, `[Conversion Rate %]`
  - Conditional formatting: Background color scale on `[ROAS]` and `[ROI %]`.

---

### Dashboard Page 2: Channel Performance
**Objective**: Channel-level diagnostic of ROI, conversion efficiency, and acquisition costs.

- **Visual 1**: *Clustered Bar Chart* (Spend vs. Revenue by Channel)
  - Y-Axis: `Marketing Channel`
  - X-Axis: `[Total Spend]`, `[Total Revenue]`
- **Visual 2**: *Scatter Chart* (Efficiency Matrix)
  - X-Axis: `[CAC]`
  - Y-Axis: `[ROAS]`
  - Bubble Size: `[Total Conversions]`
  - Details: `Marketing Channel`
- **Visual 3**: *Funnel Visual*
  - Stages: `Impressions` -> `Clicks` -> `Leads` -> `Conversions`
  - Values: `[Total Impressions]`, `[Total Clicks]`, `[Total Leads]`, `[Total Conversions]`
- **Visual 4**: *100% Stacked Bar Chart*
  - Y-Axis: `Marketing Channel`
  - X-Axis: `[Net Profit]`, `[Total Spend]` (Profitability Composition)

---

### Dashboard Page 3: Campaign Analysis
**Objective**: Granular campaign optimization, identifying star campaigns and budget bleeders.

- **Visual 1**: *Horizontal Bar Chart* (Top 10 Campaigns by Net Profit)
  - Y-Axis: `Campaign Name` (Filtered Top 10 by `[Net Profit]`)
  - X-Axis: `[Net Profit]`
  - Data labels enabled.
- **Visual 2**: *Horizontal Bar Chart* (Bottom 10 Campaigns by ROAS)
  - Y-Axis: `Campaign Name` (Filtered Bottom 10 by `[ROAS]`)
  - X-Axis: `[ROAS]`
  - Highlighted in coral/red for immediate operational review.
- **Visual 3**: *Decomposition Tree*
  - Root: `[Total Revenue]`
  - Explain By: `Marketing Channel` -> `Campaign Status` -> `Campaign Name`
- **Visual 4**: *Area Chart* (Monthly Trend by Top 5 Campaigns)
  - X-Axis: `Month_Name`
  - Y-Axis: `[Total Revenue]`
  - Legend: `Campaign Name`

---

### Dashboard Page 4: Attribution Analysis
**Objective**: Unpack customer journeys and compare First-Touch, Last-Touch, Linear, and Position-Based attribution.

- **Visual 1**: *Clustered Column Chart* (Attribution Model Revenue Comparison)
  - X-Axis: `Marketing Channel`
  - Y-Axis:
    - `[First Touch Attributed Revenue]`
    - `[Last Touch Attributed Revenue]`
    - `[Linear Attributed Revenue]`
    - `[Position Based Attributed Revenue]`
- **Visual 2**: *Waterfall Chart* (Attribution Shift: Last-Touch vs. First-Touch)
  - Category: `Marketing Channel`
  - Y-Axis: `[Attribution Shift (Last - First)]`
  - Demonstrates how Google Ads & Email gain attribution (+), while Facebook & Organic Search introduce customer journeys (-).
- **Visual 3**: *Attribution Comparison Matrix*
  - Rows: `Marketing Channel`
  - Columns: Metric Selection
  - Values: First-Touch Share %, Last-Touch Share %, Linear Share %, Position-Based Share %
- **Visual 4**: *Customer Touchpoint Depth Histogram*
  - X-Axis: `Total Touchpoints` (1, 2, 3, 4, 5)
  - Y-Axis: `Count of Customers`, `Average Conversion Rate`

---

## 5. Color Palette & Executive Theme
- **Primary Navy**: `#1F497D`
- **Secondary Slate**: `#2E5B82`
- **Success Green**: `#2ECC71`
- **Warning Amber**: `#F39C12`
- **Alert Red**: `#E74C3C`
- **Background Light**: `#F8FAFC`
- **Card Background**: `#FFFFFF` with drop shadow
