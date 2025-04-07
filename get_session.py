import lark_oapi as lark
import json
from database import Database

global_map = {}

# def get_session_by_sender_id(sender_id: str) -> str: #session: 匿名用户id
#     global global_map
#     try:
#         result = global_map[sender_id]
#     except KeyError:
#         result = ""
#     lark.logger.info(f"From sender_id: {sender_id} get session: {result}")
#     return result

def get_session_by_sender_id(sender_id: str) -> str:
    db = Database()
    return db.get_session(sender_id)

# def add_session(sender_id: str, session: str):
#     db = Database()
#     db.add_session(sender_id, session)
#     global global_map
#     global_map[sender_id] = session
#     lark.logger.info(f"Add session: {session} for sender_id: {sender_id}")

def add_session(sender_id: str, session: str):
    db = Database() #获取数据库实例
    db.add_session(sender_id, session) #添加session
    lark.logger.info(f"Add session: {session} for sender_id: {sender_id}") #记录日志
