from alpaca_trade_api.rest import REST, TimeFrame
from settings_file import ALPACA_SECRET_KEY, ALPACA_API_KEY

api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY)
data = api.get_bars('AAPL', TimeFrame.Hour, '2021-06-08', '2021-06-08', adjustment='raw').df

print(data.head())