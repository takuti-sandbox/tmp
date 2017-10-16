class Person < Struct.new(:name, :age)
  def initialize(*args)
    if args.length == 1
      super(args[0], 20)
    else
      super(*args)
    end
  end
end

p Person.new('Tom')
p Person.new('Mike', 18)
