
# echo_handler.py
from .generated import echo_pb2_grpc, echo_pb2
import logging

class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):

        logging.debug(f"Received request with message {request.message}")
        return echo_pb2.EchoReply(message=f'You said: {request.message}')
