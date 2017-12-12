a = ['x', 'y', 'z']

case ARGV[0]
when *a
  puts 'foo'
else
  puts 'bar'
end
