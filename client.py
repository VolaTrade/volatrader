from __future__ import print_function
import logging

import grpc

from src.commons.settings import SERVER_PORT
from src.generated import echo_pb2, spawn_pb2
from src.generated import echo_pb2_grpc, spawn_pb2_grpc


def run():
    with grpc.insecure_channel(f'localhost:{SERVER_PORT}') as channel:
        stub = spawn_pb2_grpc.SpawnStub(channel)
        response = stub.SpawnStrategy(spawn_pb2.SpawnRequest(sessionID="12", StrategyID="TestStrategy"))
    print("Echo client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()