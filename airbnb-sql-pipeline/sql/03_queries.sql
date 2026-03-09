-- 03_queries.sql
-- Example analytics outputs (exported by Python).

-- Average price by neighborhood (top 25)
SELECT
  neighborhood_group,
  neighborhood,
  COUNT(*) AS listings,
  ROUND(AVG(price_usd), 2) AS avg_price_usd,
  ROUND(AVG(service_fee_usd), 2) AS avg_service_fee_usd,
  ROUND(AVG(price_usd / NULLIF(availability_365,0)), 4) AS avg_price_per_available_day
FROM fct_listings
WHERE price_usd IS NOT NULL
GROUP BY neighborhood_group, neighborhood
ORDER BY avg_price_usd DESC
LIMIT 25;

-- Host leaderboard by number of listings (top 25)
SELECT
  h.host_id,
  h.host_name,
  h.host_identity_verified,
  h.calculated_host_listings_count,
  ROUND(AVG(f.price_usd), 2) AS avg_price_usd
FROM dim_host h
JOIN fct_listings f ON f.host_id = h.host_id
WHERE f.price_usd IS NOT NULL
GROUP BY h.host_id, h.host_name, h.host_identity_verified, h.calculated_host_listings_count
ORDER BY h.calculated_host_listings_count DESC
LIMIT 25;

-- Room type distribution
SELECT
  room_type,
  COUNT(*) AS listings,
  ROUND(AVG(price_usd), 2) AS avg_price_usd
FROM fct_listings
WHERE room_type IS NOT NULL
GROUP BY room_type
ORDER BY listings DESC;
