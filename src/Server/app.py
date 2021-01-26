import time as sleeper
import sys
import os
import json 
sys.path.append(os.path.dirname(os.getcwd()))
from flask import Flask, render_template, request, redirect, url_for, session
from BackTest.BackTester import backTest
from Helpers.Constants.Enums import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter
from PaperTrader.PaperTrader import PaperTrader
from Strategies.Strategies import getStratIndicators, getStratIndicatorNames, strategy
from multiprocessing import Process, Pipe, Lock
from PaperTrader import EventListener
import uuid 
from Server.WalkyTalky import WalkyTalky

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
lock = Lock()

BASE_PASSWORD = "fuck"
usernames = ['ethen', 'adrian', 'thomas', 'vitty', 'riley']

users = {username: generate_password_hash(BASE_PASSWORD + username) for username in usernames}
strat = None
started = False 

walky_talky, receiver = Pipe()
walky_talky = WalkyTalky(walky_talky)
p = Process(target=EventListener.listen, args=(receiver,))
p.start()

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route("/")
@auth.login_required
def index():
    print("------------------------------------------------------------------------------------------------------->")
    return render_template('index.html')


@app.route("/results/<pair>/<candleSize>/<strategy>/<sl>/<tp>/<time>/<principle>")
@auth.login_required
def results(pair, candleSize, strategy, sl, tp, time, principle):
    
    if session['sessionID'] is None:
        backTest(Pair[pair], Candle(candleSize), strategy, float(sl), float(tp), principle, timeStart=Time[time], server=True)

    else:
        backTest(Pair[pair], Candle(candleSize), strategy, float(sl), float(tp), principle, timeStart=Time[time], server=True, paper=session['sessionID'])
    
    print(request.args)
    # return render_template('analysis.html')


@app.route("/end", methods=['POST', 'GET'])
@auth.login_required
def endPaperTrade():
    writer = DBwriter()
    if request.method == "POST":
        item = next(request.form.items())
        key, value = item[1], item[0]
        global walky_talky
        if key == "TERMINATE":
            abort = "0" + value 
            walky_talky.walky_talky.send(abort)

        elif key == "DELETE":
            writer.deletePaperTradeSession(value)

        return redirect(url_for("papertradeRoute"))


@app.route("/backtest/strat/<strategy>", methods=['POST', 'GET'])
@auth.login_required
def updateStratParams(strategy):
    if session['type'] == "VISUALIZATION":
        global strat
        return render_template("stratupdate.html", indicators=strat.skeleton, names=strat.indicatorConstants)
    # return render_template("stratupdate.html", indicators=getStratIndicators(strategy), names=getStratIndicatorNames(strategy))


@app.route("/begin", methods=['POST', 'GET'])
@auth.login_required
def beginBackTest():
    if request.method == 'POST':
        print("REDIRECTING")
        dic = request.form
        print("---------------------------------------------------------------------->", dic)
        it = iter(request.form.values())
        print(request.form.values())
        for indicator in getStratIndicators(session['strategy']):
                print("--------------------------------------")

                for key in indicator.keys():
                    print(key)
                    try:
                        nex = float(next(it))

                    except Exception as e:
                        return render_template("invalidparam.html")
                    print("NEXT VALUE", nex)
                    indicator[key] = nex

        print("reassigned indicators ", getStratIndicators(session['strategy']))

        if session.get("type") == "BACKTEST":
            return redirect(url_for("results", pair=session.get('pair'), candleSize=session.get('candle'), strategy=session.get('strategy'), sl=session.get('stoploss'), tp=session.get('takeprofit'), principle=session.get('principle'), time=session.get('timeStart' )))

        return redirect(url_for("start_session", pair=session.get('pair'), candleSize=session.get('candle'), strategy=session.get('strategy'), sl=session.get('stoploss'), tp=session.get('takeprofit'), principle=session.get('principle'), time=session.get('timeStart' )))


@app.route("/backtest", methods=['POST', 'GET'])
@auth.login_required
def backtestRoute():
    if request.method == 'POST':
        data = request.form 
        session['pair'] = pair=request.form['pair']
        session['candle'] = candleSize=request.form['candle']
        session['strategy'] = request.form['strategy']
        session['stoploss'] = request.form['stoploss'] 
        session['takeprofit'] = request.form['takeprofit']
        session['principle'] = request.form['principle']
        session['timeStart'] = request.form['timeStart']
        session['type'] = "BACKTEST"
        session['sessionID'] = None
        return redirect(url_for("updateStratParams", strategy=request.form['strategy']))

    # return render_template('backtester.html', pairs=pairs, candles=candles, times=times, strategies=strats)

@app.route("/backtest/paper", methods=['POST', 'GET'])
@auth.login_required
def backtestPaper():
    session['pair'] = pair=request.form['pair']
    session['candle'] = candleSize=request.form['candle']
    session['strategy'] = request.form['strategy']
    session['stoploss'] = request.form['stoploss'] 
    session['takeprofit'] = request.form['takeprofit']
    session['principle'] = request.form['principle']
    session['timeStart'] = request.form['timeStart']
    session['type'] = "BACKTEST"

@app.route("/begin/<pair>/<candleSize>/<strategy>/<sl>/<tp>/<time>/<principle>")
@auth.login_required
def start_session(pair, candleSize, strategy, sl, tp, time, principle):
    print(request.args) 
    parentEnd, childEnd = Pipe()
    uid = str(uuid.uuid4())
    global walky_talky
    data = "1" + str({"pair": pair, "strategy": strategy, "candleSize": candleSize, "sl": float(sl), "tp": float(tp), "principle": principle, "time": time, "uid": uid})

    walky_talky.walky_talky.send(data)
    sleeper.sleep(1)
    global started 
    started = True 
    return redirect(url_for(('papertradeRoute')))


@app.route("/papertrade/start", methods=['POST', 'GET'])
@auth.login_required
def startPaperTrade():
    if request.method == 'POST':
        session['pair'] = request.form['pair']
        session['candle'] = request.form['candle']
        session['strategy'] = request.form['strategy']
        session['stoploss'] = request.form['stoploss'] 
        session['takeprofit'] = request.form['takeprofit']
        session['principle'] = request.form['principle']
        session['timeStart'] = request.form['timeStart']
        session['type'] = "PAPERTRADE"
        return redirect(url_for("updateStratParams", strategy=request.form['strategy']))
    # return render_template('beginpapertrade.html', pairs=pairs, candles=candles, times=times, strategies=strats)


def calculatePrinciple(sess):
    if sess['total_pnl'] == 0:
        return sess['principle']

    gain = float(sess['total_pnl']) * float(sess['principle'])
    return gain + sess['principle']



@app.route("/papertrade", methods=['POST', 'GET'])
@auth.login_required
def papertradeRoute():

    global walky_talky
    global started 
    if started:
        walky_talky.walky_talky.send("HOW ARE YOU?")
        val = walky_talky.walky_talky.recv()
        print("==================================================================== ")
        print(val)
        val = str(val)
        val = val.replace("\'", "")

        print("=----======================================")
        print(val)
        sessions = json.loads(val)


    else:
        sessions = []

        print("SESSIONS --->", sessions)

    print("SESSIONS: ", sessions)
    active, unactive = [], []

    if sessions is not None:
        for session in sessions:
            print("session ------------------> ", session)
            active.append(session)



    # return render_template('papertrader.html', active_sessions=active, unactive_sessions=unactive)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)




