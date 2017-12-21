# Map uniformly distributed random values onto gaussian distribution:
# https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform

RNG = Random.new(41)

def gaussian(mean, stddev)
  theta = 2 * Math::PI * RNG.rand
  rho = Math.sqrt(-2 * Math.log(1 - RNG.rand))
  scale = stddev * rho
  x = mean + scale * Math.cos(theta)
  y = mean + scale * Math.sin(theta)
  return x, y
end

p (1..100).each_with_object([]) {|i,a| a << gaussian(0.0, 0.1) }.flatten
