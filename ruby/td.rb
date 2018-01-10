require 'td'
require 'td-client'

cln = TreasureData::Client.new(ENV['TD_API_KEY'])
job = cln.query('sample_datasets', 'SELECT NULL, 0.0 / 0.0')
until job.finished?
  sleep 2
  job.update_progress!
end
job.update_status!
job.result_each { |row| p row }
