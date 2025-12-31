-- 02_marts.sql
-- Build dimension and fact tables.

DROP TABLE IF EXISTS dim_host;
CREATE TABLE dim_host AS
SELECT
  host_id,
  MAX(host_name) AS host_name,
  MAX(host_identity_verified) AS host_identity_verified,
  MAX(calculated_host_listings_count) AS calculated_host_listings_count
FROM stg_listings
WHERE host_id IS NOT NULL
GROUP BY host_id;

DROP TABLE IF EXISTS dim_neighborhood;
CREATE TABLE dim_neighborhood AS
SELECT
  neighborhood_group,
  neighborhood,
  COUNT(*) AS listing_count
FROM stg_listings
WHERE neighborhood IS NOT NULL
GROUP BY neighborhood_group, neighborhood;

DROP TABLE IF EXISTS fct_listings;
CREATE TABLE fct_listings AS
SELECT
  listing_id,
  host_id,
  neighborhood_group,
  neighborhood,
  room_type,
  cancellation_policy,
  instant_bookable,
  construction_year,
  price_usd,
  service_fee_usd,
  minimum_nights,
  number_of_reviews,
  reviews_per_month,
  review_rate_number,
  availability_365,
  country,
  country_code
FROM stg_listings
WHERE listing_id IS NOT NULL;
