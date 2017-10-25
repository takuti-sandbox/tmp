require 'optparse'

opts = ARGV.getopts('', 'aaa:', 'bbbb')
p opts
p opts['aaa']
p opts['bbb']
