#!/usr/bin/python
from configparser import ConfigParser
from os import environ
import os

def getFileName(environ=environ) -> str:
    if environ.get("ENV") == "prd":
        return "database_production.ini"
    
    return "database.ini"

def config(filename=getFileName(), section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    filename = filename if os.path.exists(filename) else os.path.join("..", filename)
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
