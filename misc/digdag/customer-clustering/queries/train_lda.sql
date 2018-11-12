-- @TD distribute_strategy: moderate
SELECT
  segment, factor, avg(weight) as weight
FROM (
  SELECT
    train_lda(features, '-topics ${num_topics} -iter ${iterations}')
    as (segment, factor, weight)
  FROM
    input
) t1
GROUP BY
  segment, factor
;
