select
  t1.${customer_key},
  array_concat(
    quantitative_features(
      array(
        "number of visits"
      ),
      t1.n_visits
    ),
    categorical_features(
      array(
        "td_ip_subdivision", "td_browser", "td_os", "td_language", "td_referrer"
      ),
      t1.td_ip_subdivision, t1.td_browser, t1.td_os, t1.td_language, t1.td_referrer
    ),
    t2.features
  ) as features
from
  customer_viewed_contents t1
join
  input t2
  on t1.${customer_key} = t2.${customer_key}
