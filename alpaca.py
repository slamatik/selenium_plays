from alpaca_trade_api.rest import REST, TimeFrame
from settings_file import ALPACA_SECRET_KEY, ALPACA_API_KEY
from alpaca_trade_api.stream import Stream

async def trade_callback(t):
    print(f'Trade: {t}')

async def quote_callback(q):
    print(f'Quote: {q}')


stream = Stream(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY)

stream.subscribe_trades(trade_callback, 'AAPL')
stream.subscribe_quotes(quote_callback, 'AAPL')

# stream.subscribe_trades(trade_callback, 'ETHUSD')

stream.run()