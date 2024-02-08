import websocket
import os
from dotenv import load_dotenv

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # ws.send('{"type":"subscribe","symbol":"AAPL"}')
    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

if __name__ == "__main__":
    
    load_dotenv();
    
    finhub_endpoint = os.getenv('FINHUB_ENDPOINT')
    finhub_token = os.getenv('FINHUB_TOKEN')
    
    finhub_url= finhub_endpoint + "?token=" + finhub_token
    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(finhub_url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

