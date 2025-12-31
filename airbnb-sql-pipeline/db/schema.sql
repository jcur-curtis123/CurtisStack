-- Raw landing table (lightly typed as TEXT to avoid ingestion friction)
DROP TABLE IF EXISTS raw_listings;

CREATE TABLE raw_listings (
  id TEXT,
  name TEXT,
  host_id TEXT,
  host_identity_verified TEXT,
  host_name TEXT,
  neighbourhood_group TEXT,
  neighbourhood TEXT,
  lat TEXT,
  long TEXT,
  country TEXT,
  country_code TEXT,
  instant_bookable TEXT,
  cancellation_policy TEXT,
  room_type TEXT,
  construction_year TEXT,
  price TEXT,
  service_fee TEXT,
  minimum_nights TEXT,
  number_of_reviews TEXT,
  last_review TEXT,
  reviews_per_month TEXT,
  review_rate_number TEXT,
  calculated_host_listings_count TEXT,
  availability_365 TEXT,
  house_rules TEXT,
  license TEXT
);
