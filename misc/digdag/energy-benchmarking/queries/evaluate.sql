select
  mae(predicted_electricity_consumption, annual_electricity_consumption) as mae,
  rmse(predicted_electricity_consumption, annual_electricity_consumption) as rmse
from
  prediction
