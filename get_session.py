import lark_oapi as lark
import json

global_map = {}

def get_session_by_sender_id(sender_id: str) -> str:
    global global_map
    try:
        result = global_map[sender_id]
    except KeyError:
        result = ""
    lark.logger.info(f"From sender_id: {sender_id} get session: {result}")
    return result

def add_session(sender_id: str, session: str):
    global global_map
    global_map[sender_id] = session
    lark.logger.info(f"Add session: {session} for sender_id: {sender_id}")