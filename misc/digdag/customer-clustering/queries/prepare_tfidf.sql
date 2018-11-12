WITH tf AS (
  select
    ${customer_key},
    word,
    freq
  from (
    select
      ${customer_key},
      tf(word) as word2freq
    from
      tokenized
    group by
      1
  ) t
  LATERAL VIEW explode(word2freq) t2 as word, freq
),
df AS (
  select
    word,
    count(distinct ${customer_key}) customers
  from
    tokenized
  group by
    word
),
tfidf AS (
  select
    tf.${customer_key},
    tf.word,
    tfidf(tf.freq, df.customers, ${td.last_results.n_customers}) as tfidf
  from
    tf
    JOIN df ON (tf.word = df.word)
  where
    df.customers >= 2
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
      tfidf
    )
  ) as features
from
  tfidf
group by
  1
CLUSTER by rand(43) -- random shuffling
;
