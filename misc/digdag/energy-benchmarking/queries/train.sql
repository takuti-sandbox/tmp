select
  feature,
  avg(weight) as weight
from (
  select
    train_regressor(
      features,
      annual_electricity_consumption,
      '-loss_function squared -optimizer AdaGrad -regularization l1' -- hyper-parameters
    ) as (feature, weight)
  from (
    select features, annual_electricity_consumption
    from samples
    where random_flag < 80
    CLUSTER BY rand(1) -- random shuffling
  ) t1
) t2
group by
  feature
