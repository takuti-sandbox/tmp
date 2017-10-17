def count(a, cond)
  a.inject(0) {|cnt,value| cnt += 1 if cond.call(value); cnt}
end

a = [nil, 1, 2, nil, 3]
p count(a, Proc.new {|v| v.nil?})  # count nil
p count(a, Proc.new {|v| v})  # count non-nil
