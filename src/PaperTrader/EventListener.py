from multiprocessing import Process
from Helpers.Logger import logToSlack, Channel, logDebugToFile
from Helpers.Constants.Enums import Candle, Pair, Time 
from PaperTrader.PaperTrader import PaperTrader
from threading import Thread
import json
import time 
import datetime 

def updateCheck(running_threads): 
    hasUpdated = False 

    while True: 
        minute: int = datetime.datetime.now().minute 
        
        if minute == 00 and hasUpdated is False: #hourly update
            print("hourly update")
            data = []
            for i_d in running_threads.keys():
                with open(f"{i_d}.json", "r") as fr:
                    data.append(fr.read())

            
            logToSlack( 
                        f"[HOURLY UPDATE] {str(data)}",
                        channel=Channel.PAPERTRADER
                    )
            hasUpdated = True 
            

        if minute != 00 and hasUpdated is True:
            hasUpdated = False 


def listen(reciever):

    running_threads = {}
    t = Thread(target=updateCheck, args=(running_threads,))
    t.start()

    while True:
        try:
            signal = reciever.recv()

        except Exception:
            logDebugToFile("exception reading from pipe --> ", signal)
        
        print("SIGNAL ______ ", signal)



        if signal[0] == "0": #delete
            signal = signal[1: len(signal)]
            running_threads[signal].isMegna = True 
            del running_threads[signal]


        elif signal[0] == "1": #add 
            signal = signal[1: len(signal)]
            signal = json.loads(signal.replace("\'","\""))
            p = PaperTrader(Pair[signal["pair"]], Candle(signal["candleSize"]), signal["strategy"], signal["sl"], signal["tp"], signal["principle"], Time[signal["time"]].value, signal["uid"])
            thread = Thread(target=p.run)
            thread.start()
            running_threads[signal["uid"]] = p 


        elif signal == "HOW ARE YOU?":
            data = []
            for i_d in running_threads.keys():
                with open(f"{i_d}.json", "r") as fr:
                    data.append(fr.read())

            reciever.send(data)



