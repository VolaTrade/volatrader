# main.py
from src.app import Server
from src.commons.logger import get_logger
from src.commons.settings import SERVER_PORT
import logging
import sys

def main():
    logger = get_logger()
    logger.debug(f"Starting grpc server at port :{SERVER_PORT}")
    Server.run()

main()
