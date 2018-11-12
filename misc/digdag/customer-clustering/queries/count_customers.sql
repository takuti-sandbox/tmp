select
  count(distinct ${customer_key}) as n_customers
from
  customer_viewed_contents
