select
  segment,
  to_ordered_list(factor, rnk) as factors
from
  ranked_words
group by
  segment
order by
  segment asc
;
