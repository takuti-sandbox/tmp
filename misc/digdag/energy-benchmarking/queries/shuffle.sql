select
  *,
  abs(from_big_endian_64(xxhash64(to_big_endian_64(id))) % 100) as random_flag
from
  vectors
