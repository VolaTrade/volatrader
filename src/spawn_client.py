#spawn_client.py 
from .generated import spawn_pb2_grpc, spawn_pb2
from .commons.globals import LiveStrategies, get_strategy
from .commons.status_codes import StatusCode
import logging

not_valid = lambda value: True if value is None else False

def gen_spawn_response(success: bool, message: str, code: StatusCode):
    response = spawn_pb2.SpawnReply(
                            success=success,
                            message=message,
                            code=code
                            )
    logging.debug(response)
    return response


class Spawner(spawn_pb2_grpc.SpawnServicer):

    def SpawnStrategy(self, request, context):

        logging.debug(f"sessionID: {request.sessionID} , strategyID: {request.StrategyID}")
        if not_valid(request.sessionID):
            return gen_spawn_response(False, "SessionID missing", StatusCode.INVALID_ARGUMENT.value)

        if not_valid(request.StrategyID):
            return gen_spawn_response(False, "StrategyID missing", StatusCode.INVALID_ARGUMENT.value)
        if request.sessionID in LiveStrategies:
            return gen_spawn_response(False, "Session already exists", StatusCode.ALREADY_EXISTS.value)

        strategy_class = None 
        try: 
            strategy_class = get_strategy(request.StrategyID)

        except Exception as e:
            logging.error(e)
            return gen_spawn_response(False, "Strategy provided not found", StatusCode.NOT_FOUND.value)

        LiveStrategies[request.sessionID] = strategy_class
        return gen_spawn_response(True, "Ok", StatusCode.OK.value)




