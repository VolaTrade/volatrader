import argparse
from PaperTrader.PaperTrader import PaperTrader
from Helpers.Constants.Enums import Time, Candle, Pair
from Helpers.Logger import logToSlack
from DataBasePY.DBwriter import DBwriter
from Helpers.ArgParser import getParser

def main(args):
	paper_trader = PaperTrader()
	writer = DBwriter()

	try:
		paper_trader.trade(args.pair, args.candlesize, args.strategy, args.stoploss, args.takeprofit, args.principle, Time[args.time].value)

	except KeyboardInterrupt:
		writer.writePaperTradeEnd(paper_trader.sessionid)
		logToSlack(f"Finished papertrader session with id {paper_trader.sessionid}")

	except Exception as e:
		logToSlack(e)


if __name__ == '__main__':
	args = getParser()
	main(args)
