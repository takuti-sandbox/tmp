WITH ranked as (
  select
    segment,
    factor,
    weight,
    dense_rank() OVER (PARTITION BY segment ORDER BY weight DESC) AS rnk
  from
    lda_model
)
SELECT
  *
FROM
  ranked
WHERE
  rnk <= ${topk_rank}
ORDER BY
  segment ASC, rnk ASC
;
