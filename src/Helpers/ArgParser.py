import argparse


def getParser():
    parser = argparse.ArgumentParser(description="Use this to backtest your strategies")
    parser.add_argument('-p', '--pair', type=Pair, required=True,
                    help='Pair to backtest for. Reference Enums.py for more details')
    parser.add_argument('--candleSize', '-candle', type=Candle, required=True,
                    help="Candle size to get data for (5m, 15m, 30m, etc)")
    parser.add_argument('--strategy', '-strat', type=str, required=True,
                    help="Strategy to backtest")
    parser.add_argument('-sl', '--stoploss', type=int, default=1,
                    help="Trailing stop loss percentage")
    parser.add_argument('-tp', '--takeprofit', type=int, default=2,
                    help="Take profit percentage")
    parser.add_argument('--principle', '-investment', type=int, default=10000,
                    help="Starting capital")
    parser.add_argument('--readFromDatabase', type=bool, default=False,
                    help="Reads from database if true, otherwise gets live candle data from API")
    parser.add_argument('--outputGraph', type=bool, default=True,
                    help="Outputs backtest results into csv if true, otherwise does not")
    parser.add_argument('-t','--time', type=str, default="MONTH",
                    help="Total time to backtest on")

    parser.add_argument("--market", type=str, default="BINANCE")

    return parser.parse_args()
    