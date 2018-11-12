select
  t1.${customer_key}, t1.segment,
  t2.factors as top_relevant_factors
from
  predicted_topics t1
join
  topic_words t2
  on t1.segment = t2.segment
