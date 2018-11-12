WITH word_counts as (
  select
    ${customer_key},
    word,
    count(1) as cnt
  from
    tokenized
  group by
    1, 2
)
-- DIGDAG_INSERT_LINE
select
  ${customer_key},
  collect_list(
    feature(
      concat(
        'keyword#',
        translate(word,':','\;')
      ),
      cnt
    )
  ) as features
from
  word_counts
where
  cnt >= 2
group by
  1
CLUSTER by rand(43) -- random shuffling
;
