from telegram.ext import Updater, InlineQueryHandler, CommandHandler
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
    TESTING = "-1001268092194"
    PRODUCTION = ""

class MessageType(Enum):
    BUY_NOTIF = 0
    SELL_NOTIF = 1
    MEMBER_WELCOME = 2



def wrapMessage(pair: Pair, candle: Candle, market: Market, sug_sl: float, sug_tp: float, message_type: MessageType) -> None:
    link_pair = pair.value.replace("/","")
    if message_type == MessageType.BUY_NOTIF:
        print("sending message")
        sendMessage(
                        f"🚨🔔 BUY SIGNAL DETECTED 🚨🔔\
                        \n🚨  {pair.value}/{candle.value} 🚨\
                        \n🚨  SUGGESTED STOP : {sug_sl}% 🚨\
                        \n🚨  SUGGESTED TAKEP : {sug_tp}% 🚨\
                        \n🚨www.binance.com/en/trade/{link_pair} 🚨",      

                    Chat.TESTING)

def sendMessage(text: str, chat_id: Chat) -> None:
    resp = requests.post(f"https://api.telegram.org/bot1210339133:AAGQyx5k8x_5cdQTmy8d3CU6sT0fod4gEPQ/sendMessage?chat_id={chat_id.value}&text={text}")





    #  \n🎉WELCOME NEW MEMBER!🎉\
    #                     \nMember Name:"


wrapMessage(Pair.ETHUSDT, Candle.FIFTEEEN_MINUTE, Market.BINANCE, 2, 4, MessageType.BUY_NOTIF)