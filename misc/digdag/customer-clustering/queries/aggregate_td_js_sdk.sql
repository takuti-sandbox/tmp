select
  ${customer_key},
  array_join(array_agg(td_title), ' ') as contents,
  ln(count(1) + 1) as n_visits,
  td_ip_to_least_specific_subdivision_name(max_by(td_ip, time)) as td_ip_subdivision,
  max_by(td_browser, time) as td_browser,
  max_by(td_os, time) as td_os,
  max_by(substr(td_language, 1, 2), time) as td_language,
  max_by(regexp_extract(td_referrer, '^https?://([^/]+).*', 1), time) as td_referrer
from
  ${source_database}.${source_table}
group by
  1
