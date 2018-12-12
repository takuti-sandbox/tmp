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
  ) as features,
  electricity_use__kbtu_ as annual_electricity_consumption
from
  mbed_connect.energy_benchmarking
where
  electricity_use__kbtu_ is not null
