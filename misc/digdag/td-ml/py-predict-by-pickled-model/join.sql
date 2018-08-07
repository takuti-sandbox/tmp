select
  t1.*,
  t2.predict
from
  churn t1
join
  churn_predict t2
  on t1.phone = t2.key
