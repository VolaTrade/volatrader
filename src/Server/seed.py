import time as sleeper
import sys
import os
import json 
sys.path.append(os.path.dirname(os.getcwd()))
from multiprocessing import Pipe, Process 

from PaperTrader import EventListener


if __name__ == '__main__':
    walky_talky, childEnd = Pipe()
    p = Process(target=EventListener.listen, args=(childEnd,))
    p.start()

    
    while True: 
        sleeper.sleep(5)

        walky_talky.send("DUMMY")

    p.join()