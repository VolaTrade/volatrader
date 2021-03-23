# app.py
from concurrent import futures
import grpc
import logging
from .generated import echo_pb2_grpc, spawn_pb2_grpc
from .echo_client import Echoer
from .spawn_client import Spawner
from .commons.settings import SERVER_PORT, MAX_THREADS
class Server:
    
    @staticmethod
    def run():
        logging.debug(f"Setting max threads to: {MAX_THREADS}")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_THREADS))
        echo_pb2_grpc.add_EchoServicer_to_server(Echoer(), server)
        spawn_pb2_grpc.add_SpawnServicer_to_server(Spawner(), server)
        server.add_insecure_port(f"[::]:{SERVER_PORT}")
        server.start()
        server.wait_for_termination()
