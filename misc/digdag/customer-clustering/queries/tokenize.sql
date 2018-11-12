WITH exploded as (
  select
    t1.${customer_key},
    singularize(t2.word) as word
  from
    customer_viewed_contents t1 LATERAL VIEW explode(tokenize(contents,true)) t2 as word
)
-- DIGDAG_INSERT_LINE
select
  l.${customer_key},
  l.word
from
  exploded l
where
  NOT is_stopword(l.word) AND
  length(l.word) >= 2 AND cast(l.word AS double) IS NULL
;
