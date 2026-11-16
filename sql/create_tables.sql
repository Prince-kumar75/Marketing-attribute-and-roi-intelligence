-- ==============================================================================
-- Marketing Attribution and ROI Intelligence
-- Database Schema Definition (PostgreSQL / MySQL Compatible)
-- ==============================================================================

-- Drop tables if they already exist
DROP TABLE IF EXISTS customer_attribution_touchpoints;
DROP TABLE IF EXISTS marketing_campaigns;

-- 1. Fact Table: Marketing Campaign Performance Logs
CREATE TABLE marketing_campaigns (
    campaign_id                 VARCHAR(30)     NOT NULL,
    campaign_name               VARCHAR(150)    NOT NULL,
    marketing_channel           VARCHAR(50)     NOT NULL,
    campaign_status             VARCHAR(20)     NOT NULL,
    campaign_date               DATE            NOT NULL,
    year                        INT             NOT NULL,
    month                       INT             NOT NULL,
    month_name                  VARCHAR(10)     NOT NULL,
    month_year                  VARCHAR(7)      NOT NULL,
    quarter                     VARCHAR(5)      NOT NULL,
    day_of_week                 VARCHAR(15)     NOT NULL,
    marketing_spend             NUMERIC(12, 2)  NOT NULL DEFAULT 0.00,
    impressions                 BIGINT          NOT NULL DEFAULT 0,
    clicks                      BIGINT          NOT NULL DEFAULT 0,
    leads                       BIGINT          NOT NULL DEFAULT 0,
    conversions                 BIGINT          NOT NULL DEFAULT 0,
    revenue                     NUMERIC(14, 2)  NOT NULL DEFAULT 0.00,
    net_profit                  NUMERIC(14, 2)  NOT NULL DEFAULT 0.00,
    roi                         NUMERIC(10, 2)  NOT NULL DEFAULT 0.00,
    roas                        NUMERIC(10, 2)  NOT NULL DEFAULT 0.00,
    customer_acquisition_cost   NUMERIC(10, 2)  NOT NULL DEFAULT 0.00,
    conversion_rate             NUMERIC(8, 2)   NOT NULL DEFAULT 0.00,
    cpc                         NUMERIC(8, 2)   NOT NULL DEFAULT 0.00,
    cpl                         NUMERIC(8, 2)   NOT NULL DEFAULT 0.00,
    ctr                         NUMERIC(8, 2)   NOT NULL DEFAULT 0.00,
    customer_id                 VARCHAR(30)     NOT NULL
);

-- Indexes for performance optimization on large query workloads
CREATE INDEX idx_campaigns_channel ON marketing_campaigns(marketing_channel);
CREATE INDEX idx_campaigns_date ON marketing_campaigns(campaign_date);
CREATE INDEX idx_campaigns_status ON marketing_campaigns(campaign_status);
CREATE INDEX idx_campaigns_camp_id ON marketing_campaigns(campaign_id);
CREATE INDEX idx_campaigns_month_year ON marketing_campaigns(month_year);

-- 2. Touchpoint Table: Multi-Touch Customer Journey Touchpoints
CREATE TABLE customer_attribution_touchpoints (
    touchpoint_id               SERIAL PRIMARY KEY,
    customer_id                 VARCHAR(30)     NOT NULL,
    touchpoint_sequence         INT             NOT NULL,
    total_touchpoints           INT             NOT NULL,
    touchpoint_timestamp        TIMESTAMP       NOT NULL,
    touchpoint_date             DATE            NOT NULL,
    marketing_channel           VARCHAR(50)     NOT NULL,
    campaign_name               VARCHAR(150)    NOT NULL,
    journey_converted           SMALLINT        NOT NULL DEFAULT 0,
    is_conversion_touchpoint    SMALLINT        NOT NULL DEFAULT 0,
    conversion_revenue          NUMERIC(12, 2)  NOT NULL DEFAULT 0.00,
    total_journey_revenue       NUMERIC(12, 2)  NOT NULL DEFAULT 0.00
);

CREATE INDEX idx_touchpoints_customer ON customer_attribution_touchpoints(customer_id);
CREATE INDEX idx_touchpoints_channel ON customer_attribution_touchpoints(marketing_channel);
CREATE INDEX idx_touchpoints_converted ON customer_attribution_touchpoints(journey_converted);
CREATE INDEX idx_touchpoints_seq ON customer_attribution_touchpoints(customer_id, touchpoint_sequence);
