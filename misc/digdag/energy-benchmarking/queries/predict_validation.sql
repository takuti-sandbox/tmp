with features_exploded as (
  select
    id,
    extract_feature(fv) as feature,
    extract_weight(fv) as value
  from (
    select * from samples where random_flag >= 80
  ) t1
  LATERAL VIEW explode(features) t2 as fv
)
-- DIGDAG_INSERT_LINE
select
  t1.annual_electricity_consumption,
  t2.predicted_electricity_consumption
from
  samples t1
join (
    select
      t1.id,
      sum(p1.weight * t1.value) as predicted_electricity_consumption
    from
      features_exploded t1
      LEFT OUTER JOIN model p1 ON (t1.feature = p1.feature)
    group by
      t1.id
  ) t2
  on t1.id = t2.id
