from Helpers.Constants.Enums import Pair, Candle
from DataBasePY.DBoperations import DBoperations
from Helpers.Logger import logDebugToFile, logErrorToFile
import json
import re
from typing import Dict, List


class DBReader(DBoperations):
	"""
	DataBase reader class that performs read operations on coin-database
	@:inherited from DBoperations
	"""

	def __init__(self):
		super().__init__()

	def getPaperTradeSessions(self) -> List[Dict[str, str]]:
		query: str = 'select row_to_json(t) from (SELECT * FROM papertrader_results) t;'

		try:
			raw_data: str = str(self.readExecute(query))
			# logDebugToFile(raw_data)
			values: List[Dict[str, str]] = json.loads(raw_data.replace("(", "").replace(",)", "").replace("\'", "\"").replace("None,", "\"None\",").replace("True", "\"True\"").replace("False", "\"False\""))
			print("PAPER TRADE SESSIONS: ", values)
			return values

		except Exception as e:
			print(e)
			logErrorToFile(e)

	def getPaperTradeSession(self, sessionId: str) -> Dict[str, str]:
		query: str = 'SELECT (transactions) FROM papertrader_results WHERE session_id = %s;'
		params: tuple = (sessionId, )
		try:
			raw_data: str = self.readExecute(query, params)
			values: Dict[str, str] = json.loads(str(raw_data).replace("(", "").replace(")", "").replace("\'", "\"").replace(",]", "]").replace("[[", "[").replace("]]", "]"))
			return values

		except Exception as e:
			print(e)
			logErrorToFile(e)


	def readVolumeData(self, pair: Pair, candle: Candle) -> tuple:
		query: str = "SELECT mean_volume, volume_sd FROM STATISTIC_TABLE WHERE pair = %s AND candle = %s;"
		params: tuple = (pair.value, candle.value)

		try:
			raw_data: str = self.readExecute(query, params)
			return raw_data

		except Exception as e:
			print(e)
			logErrorToFile(e)

	def getAllSessionInfo(self, sessionId: str) -> Dict[str, str]:
		query: str = f'SELECT (pair, candle, strategy, stoploss, takeprofit, principle, indicators) FROM papertrader_results WHERE session_id =%s;'
		tup: tuple = (sessionId, )
		try:
			raw_data: str = self.readExecute(query, tup)
			values: Dict[str, str] = json.loads(str(raw_data).replace("(", "").replace(")", "").replace("\'", "\"").replace(",]", "]").replace("[[", "[").replace("]]", "]"))
			return values 

		except Exception as e:
			print(e)
			logErrorToFile(e)


	def getActiveStatus(self, sessionId: str) -> bool:
		"""
		@param: sessionID: unique ID to reference session
		@returns: active status of session
		"""
		# sessionId = str(sessionId)
		query: str = 'SELECT active FROM papertrader_results WHERE session_id = %s;'
		tup: tuple = (sessionId, )

		try:
			raw_data: str = self.readExecute(query, tup)
			return True if str(raw_data).find("T") != -1 else False

		except Exception as e:
			logErrorToFile(e)

	def getSupportResistance(self, pair: Pair, candle: Candle): #TODO finish
		"""
		@param: pair, candle: Enums to specify which support/resistance strategies to obtain
		@returns: current support/resistance of given pair, candle
		"""
		query: str = "SELECT ROW_to_JSON(t) FROM (SELECT support, resistance FROM support_resistance WHERE pair=\'%s\' AND candle=\'%s\') t;"
		tup: tuple = (pair.value, candle.value)
		
		try:
			self.execute(query, self.paramsToTuple(tup))
			regex = re.compile("{.+}")
			values = json.loads(regex.search(str(self.cur.fetchall())).group().replace("\'", "\""))
			self.terminateConnection()
			return values

		except Exception as e:
			logErrorToFile(e)


	def getStrategySource(self, strat_name: str):
		query: str = "SELECT version_number, source FROM STRATEGIES WHERE strategy = %s ORDER BY version_number DESC LIMIT 1;"
		param: tuple = (strat_name,)

		try:
			data: str = self.readExecute(query, param)
			return data[0]

		except Exception as e:
			logErrorToFile(e)
			raise e 


	def getTrackingUsers(self, session_id: str):
		fetch_query: str = 'SELECT users_tracking FROM papertrader_results WHERE session_id = %s;'
		params: tuple = (session_id,)
		data: str = ""		
		try:
			data = self.readExecute(fetch_query, params)
		except Exception as e:
			raise e 

		print("Fetched Data", data)
		data = json.loads(str(data)[2 : len(data) - 4].replace("\'", "\""))
		return data 
