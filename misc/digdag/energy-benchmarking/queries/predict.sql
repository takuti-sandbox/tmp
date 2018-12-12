with null_samples as (
  select
    id,
    array_concat(
      categorical_features(
        array('Chicago community area', 'Primary use of property'),
        community_area, primary_property_type
      ),
      quantitative_features(
        array('Total interior floor space', 'Building age', 'Number of buildings'),
        gross_floor_area___buildings__sq_ft_, data_year - year_built, num_of_buildings
      )
    ) as features
  from
    chicago_smart_green.energy_benchmarking
  where
    electricity_use__kbtu_ is null
),
features_exploded as (
  select
    id,
    extract_feature(fv) as feature,
    extract_weight(fv) as value
  from null_samples t1
  LATERAL VIEW explode(features) t2 as fv
)
select
  t1.id,
  sum(p1.weight * t1.value) as predicted_electricity_consumption
from
  features_exploded t1
  LEFT OUTER JOIN model p1 ON (t1.feature = p1.feature)
group by
  t1.id
