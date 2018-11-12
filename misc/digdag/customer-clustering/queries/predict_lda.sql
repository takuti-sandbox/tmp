-- @TD reducers: 10
WITH exploded as (
  select
    l.${customer_key},
    extract_feature(feature) as factor,
    extract_weight(feature) as value
  from
    input l
    LATERAL VIEW explode(features) r as feature
),
predicted as (
  select
    t.${customer_key},
    lda_predict(t.factor, t.value, m.segment, m.weight, '-topics ${num_topics}') as probabilities
  from
    exploded t
    JOIN lda_model m ON (t.factor = m.factor)
  group by
    1
)
-- DIGDAG_INSERT_LINE
select
  ${customer_key},
  probabilities[0].label as segment
from
  predicted
;
