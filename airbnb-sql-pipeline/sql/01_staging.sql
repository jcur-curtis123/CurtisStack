-- 01_staging.sql
-- Create a cleaned, typed staging table from raw_listings.

DROP TABLE IF EXISTS stg_listings;

CREATE TABLE stg_listings AS
SELECT
  CAST(NULLIF(id,'') AS INTEGER)                        AS listing_id,
  NULLIF(TRIM(name),'')                                 AS listing_name,

  CAST(NULLIF(host_id,'') AS INTEGER)                   AS host_id,
  CASE
    WHEN LOWER(TRIM(host_identity_verified)) IN ('t','true','yes','verified') THEN 1
    WHEN LOWER(TRIM(host_identity_verified)) IN ('f','false','no','unverified') THEN 0
    ELSE NULL
  END                                                   AS host_identity_verified,
  NULLIF(TRIM(host_name),'')                            AS host_name,

  NULLIF(TRIM(neighbourhood_group),'')                  AS neighborhood_group,
  NULLIF(TRIM(neighbourhood),'')                        AS neighborhood,

  CAST(NULLIF(lat,'') AS REAL)                          AS latitude,
  CAST(NULLIF(long,'') AS REAL)                         AS longitude,

  NULLIF(TRIM(country),'')                              AS country,
  NULLIF(TRIM(country_code),'')                         AS country_code,

  CASE
    WHEN LOWER(TRIM(instant_bookable)) IN ('t','true','yes','1') THEN 1
    WHEN LOWER(TRIM(instant_bookable)) IN ('f','false','no','0') THEN 0
    ELSE NULL
  END                                                   AS instant_bookable,

  NULLIF(TRIM(cancellation_policy),'')                  AS cancellation_policy,
  NULLIF(TRIM(room_type),'')                            AS room_type,

  CAST(NULLIF("construction_year",'') AS INTEGER)       AS construction_year,

  -- Remove '$' and commas, then cast
  CAST(NULLIF(REPLACE(REPLACE(TRIM(price),'$',''),',',''),'') AS REAL)        AS price_usd,
  CAST(NULLIF(REPLACE(REPLACE(TRIM(service_fee),'$',''),',',''),'') AS REAL)  AS service_fee_usd,

  CAST(NULLIF("minimum_nights",'') AS INTEGER)          AS minimum_nights,
  CAST(NULLIF("number_of_reviews",'') AS INTEGER)       AS number_of_reviews,

  NULLIF(TRIM("last_review"),'')                        AS last_review,  -- keep as TEXT; parse in downstream tools if needed

  CAST(NULLIF("reviews_per_month",'') AS REAL)          AS reviews_per_month,
  CAST(NULLIF("review_rate_number",'') AS REAL)         AS review_rate_number,

  CAST(NULLIF("calculated_host_listings_count",'') AS INTEGER) AS calculated_host_listings_count,
  CAST(NULLIF("availability_365",'') AS INTEGER)        AS availability_365,

  NULLIF(TRIM("house_rules"),'')                        AS house_rules,
  NULLIF(TRIM("license"),'')                            AS license
FROM raw_listings
WHERE NULLIF(id,'') IS NOT NULL;
