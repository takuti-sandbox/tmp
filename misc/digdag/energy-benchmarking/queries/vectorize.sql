select
  id,
  array_concat(
    categorical_features(
      array('Chicago community area', 'Primary use of property'),
      if(community_area = 'LOOP', 'LOOP', 'Others'),
      if(primary_property_type = 'Office', 'Office', 'Others')
    ),
    quantitative_features(
      array('Total interior floor space', 'Building age', 'Number of buildings'),
      ln(gross_floor_area___buildings__sq_ft_ + 1),
      ln(data_year - year_built + 1),
      ln(num_of_buildings + 1)
    )
  ) as features,
  (electricity_use__kbtu_ / 1000000.0) as annual_electricity_consumption
from
  mbed_connect.energy_benchmarking
where
  electricity_use__kbtu_ is not null
