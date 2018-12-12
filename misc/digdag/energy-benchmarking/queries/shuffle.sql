select
  *,
  abs(from_big_endian_64(xxhash64(to_utf8(cast(id as varchar)))) % 100) as random_flag
from
  vectors
