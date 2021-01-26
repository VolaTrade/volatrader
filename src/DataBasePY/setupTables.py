import os 
import sys
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from DataBasePY.config import config
import psycopg2
from Helpers.Constants.Enums import Candle, Pair, Strategy

pgEnumTypes = [Candle, Pair, Strategy]


def buildPgEnumStr(pgType: str, enumList: list):
    enumListStr = "\', \'".join(enumList)
    return f"CREATE TYPE {pgType} AS ENUM ('{enumListStr}');"


def createEnumTypes(pgEnums):
    return [buildPgEnumStr(pgEnum.__name__.lower(), [pgType.value for pgType in pgEnum]) for pgEnum in pgEnums]


def readRefs():
    try:
        with open("references.sql", "r") as fp:
            lines: str = fp.read()
            return lines
    except Exception as e:
        print('ERROR READING TABLE CREATION QUERIES')
        raise e


def buildQueries():
    lines = readRefs()
    enums = createEnumTypes(pgEnumTypes)
    print(enums)
    return [*enums, lines]


def createConnection():
    print("Connecting to PostgreSQL Database")
    conn, params = None, None
    try:
        params = config()
        print("params -----> ", params)
        conn = psycopg2.connect(**params)

    except Exception as e:
        print("--------------- FAILED -------------")
        print("Error caught trying to initialize db config params")
        raise e

    return conn


def executeAll(queries):
    conn = createConnection()
    conn.autocommit = True
    cursor = conn.cursor()
    for query in queries:
        try:
            cursor.execute(query)
        except psycopg2.errors.DuplicateObject as e:
            print(e)

    conn.commit()
    conn.close()


def run():
    queries = buildQueries()
    try:
        executeAll(queries)
        print("--------------- SUCCESS -------------- ")
    except Exception as e:
        print(f"--------------- FAILED --------------\n{e}")


if __name__ == '__main__':
    run()
