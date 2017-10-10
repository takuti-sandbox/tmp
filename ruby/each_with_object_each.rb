%w[a b c].each_with_object([]) do |elem, ary|
  ary << elem.downcase
  ary << elem.upcase
end.each do |elem|
  puts elem
end
