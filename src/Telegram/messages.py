import requests
import re
import os 
import sys
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from enum import Enum 
from Helpers.Constants.Enums import Pair, Candle, Market 
import requests 



class Chat(Enum):
    PRODUCTION = os.environ.get("TELEGRAM_CHANNEL_PRODUCTION")
    TESTING = os.environ.get("TELEGRAM_CHANNEL_TESTING")

class MessageType(Enum):
    BUY_NOTIF = 0
    SELL_NOTIF = 1
    MEMBER_WELCOME = 2



def wrapMessage(pair: Pair, candle: Candle, market: Market, sug_sl: float, sug_tp: float, tradeId: str, message_type: MessageType=MessageType.BUY_NOTIF) -> None:
    link_pair = pair.value.replace("/","")
    if message_type == MessageType.BUY_NOTIF:
        sendMessage(
                        f"🚨🔔 BUY SIGNAL DETECTED 🔔🚨\
                        \n{pair.value}/{candle.value}\
                        \nSuggested Stop : ${sug_sl}\
                        \nSuggested TakeProfit : ${sug_tp}\
                        \nTrade ID : {tradeId}\
                        \nwww.binance.com/en/trade/{link_pair}", 
                             

                    Chat.TESTING if os.environ.get("DEBUG") == "True" else Chat.PRODUCTION)

def sendMessage(text: str, chat_id: Chat) -> None:
    bot = os.environ.get("TELEGRAM_BOT_TOKEN")
    resp = requests.post(f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id.value}&text={text}")




def sendTradeExit(chat_ids: list, session_id: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    for chat_id in chat_ids:
        print("sending exit", chat_id)
        resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=Exit detected for {session_id}")
