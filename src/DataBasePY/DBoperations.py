import psycopg2
from Helpers.DataOperators import convertCandlesToDict
from Helpers.Constants.Enums import Candle, Pair
from DataBasePY.config import config
from Helpers.Logger import logToSlack, logDebugToFile, MessageType
from multiprocessing import Lock
import time 

class DBoperations:
	"""
	Base database operations class for handling Database connection, commits, & ensuring connection
	"""

	def __init__(self):
		self.conn = None
		self.cur = None
		self.database_lock = Lock()
		self.file_lock = Lock()
		self.CONNECTIONS_LIMIT: int = 22


	def setCur(self, cur):
		self.cur = cur 


	def writeExecute(self, query: str, queryParams: tuple, retry: int=3, psycopg2=psycopg2) -> None:
		
		try:
			params = config()
			print("PERFORMING WRITE EXECUTION")
			print(f"EXECUTING {query}")
			self.conn = psycopg2.connect(**params)
			self.cur = self.conn.cursor()


		except Exception as e:
				raise e

		try:
			self.database_lock.acquire()
			print(f"Executing query: {query} with params: {queryParams}")
			self.cur.execute(query, queryParams)
			self.commit()

		except Exception as e:
			print("Error executing query: ", e)
			raise e

		finally:
			self.database_lock.release()
			print(f"FINISHED QUERY: {query}")

	def readExecute(self, query: str, queryParams: [tuple, None] = None, retry: int = 3) -> list:
		
		try:
			params = config()
			print("PERFORMING READ QUERY: ", query)
			self.conn = psycopg2.connect(**params)
			self.cur = self.conn.cursor()

			try:
				if queryParams is None:
					self.cur.execute(query)
				else:
					self.cur.execute(query, queryParams)
				return self.cur.fetchall()

			except Exception as e:
				print('ERROR READING FROM DB: ', e)
				if retry > 0:
					print(f"RETRYING READ QUERY {retry} more times...")
					self.readExecute(query, queryParams, retry-1)
				else:
					print("Recursive retry limit exceeded .... dumbass")
					raise e


		except Exception as e:
			print("Error executing query: ", e)
			raise e

		finally:
			self.terminateConnection()

	def commit(self) -> None:
		""""
		Commits cursor data to Database .. alters || adds to table 
		@:returns None
		"""

		print("Comitting to database\n")
		self.conn.commit()
		self.terminateConnection()
		print("success :0")

	def connect(self) -> (None, Exception):
		"""
		connects to DataBase
		@:returns None if connection is successful
		@:returns Exception otherwise
		"""

		try:
			params = config()
			# print("Connecting to postgreSQL database")
			self.conn = psycopg2.connect(**params)
			self.cur = self.conn.cursor()

		except(Exception, psycopg2.DatabaseError) as error:
			print("Error : ", error)
			return error

		return None

	def connStatus(self):
		"""
		@:returns connection status
		"""

		return self.conn

	def terminateConnection(self) -> None:
		"""
		closes connection w/ database
		"""
		self.conn.close()

	def ensureConnection(self):
		"""
		 ensures connection is still bounded
		"""

		if self.connStatus() is None:
			self.connect()