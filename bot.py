from config import Config
import lark_oapi as lark
from message import send_message_to_group
from forward import forward_message_to_group
from message_get import get_message_from_group
from get_session import get_session_by_sender_id, add_session
from reply import reply_message_to_group
import json
from uuid import uuid4

class Bot:
    def __init__(self, config_path: str = "config.toml"):

        # 配置
        self.config = Config.load(config_path)

        # 飞书客户端
        self.client = lark.Client.builder()\
            .app_id(self.config.lark.app_id)\
            .app_secret(self.config.lark.app_secret)\
            .build()
        
        # 注册事件处理函数
        event_handler = lark.EventDispatcherHandler.builder("", "") \
            .register_p2_im_message_receive_v1(self.handle_message_receive) \
            .build()
        
        # 飞书 websocket 客户端，建立双工通道，接收飞书事件
        self.ws = lark.ws.Client(
            self.config.lark.app_id,
            self.config.lark.app_secret,
            event_handler=event_handler,
            log_level=self.config.log_level
        )
        
    def handle_message_receive(self, event: lark.im.v1.P2ImMessageReceiveV1):
        '''
        处理飞书消息接收事件

        Args:
            event: 飞书消息接收事件

        See Also:
            - [飞书开放平台-接收消息](https://open.feishu.cn/document/server-docs/im-v1/message/events/receive)
            - [飞书开放平台-接收消息内容](https://open.feishu.cn/document/server-docs/im-v1/message-content-description/message_content)
            - [飞书开放平台-处理事件](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/handle-events)
        '''
        chat_type = event.event.message.chat_type
        if chat_type != "p2p":
            return
        content = json.loads(event.event.message.content)
        message_type = event.event.message.message_type
        message_id = event.event.message.message_id
        sender_id = event.event.sender.sender_id.open_id
        p2p_chat_id = event.event.message.chat_id

        lark.logger.info(f"Received message: {content}")
        self.handle_message(message_id, sender_id, p2p_chat_id)

#         if message_type == "text":
#             match content["text"]:
#                 case "/generate":
#                     '''
#                     指令"/generate"用于随机生成匿名ID
#                     '''
#                     session = str(uuid4())
#                     add_session(sender_id, session)
#                 case "/help":
#                     text = '''/help           查看帮助信息
# /generate     用于随机生成匿名ID   
# /name abc    用于设置匿名ID为abc
# 若未设置匿名ID,则会随机生成'''
#                     send_message_to_group(self.client, p2p_chat_id, text)
#                 case _:
#                     command: str = content["text"]
#                     '''
#                     指令"/name abc"用于设置匿名ID为abc
#                     '''
#                     if command.startswith("/name "):
#                         session = command[6:]
#                         session = session.strip()
#                         add_session(sender_id, session)
#                     else:
#                         self.handle_message(message_id, sender_id, p2p_chat_id)
#         else:
#             self.handle_message(message_id, sender_id, p2p_chat_id)

    def start(self):
        self.ws.start()

    '''
    转发消息,并判断并执行是否在消息前增加匿名ID消息
    '''
    def handle_message(self, message_id: str, sender_id: str, p2p_chat_id: str):

        session: str = get_session_by_sender_id(sender_id) # 如果没有匿名ID,则返回空字符串
        if session == "":
            session = str(uuid4()) #新建session TODO: 根据时间生成session
            add_session(sender_id, session)
            # new_message = f"已自动创建匿名ID: {session}"
            # send_message_to_group(self.client, p2p_chat_id, new_message)


        if self.config.chat_type == "chat": #处理群聊中是否需要添加title
            should_title = True
            response : lark.im.v1.ListMessageResponseBody = get_message_from_group(self.client, self.config.chat_id)
            current_messages = response.items # 获取当前群聊中最近的十条消息
            for current_message in current_messages:
                current_content = json.loads(current_message.body.content)
                current_msg_type = current_message.msg_type
                sender_type = current_message.sender.sender_type
                if sender_type == "user":
                    should_title = True
                    break
                if current_msg_type != "text":
                    continue
                sentence: str = current_content["text"]
                if sentence.startswith("[匿名ID]"):
                    this_session = sentence[6:]
                    if this_session == session:
                        should_title = False
                        break
                    else:
                        should_title = True
                        break
                else:
                    continue

            if should_title:
                title = "[匿名ID]{}".format(session)
                send_message_to_group(self.client, self.config.chat_id, title)

        forward_response_data = forward_message_to_group(self.client, self.config.chat_id, message_id)

        # if self.config.chat_type == "thread":
        #     title = "[匿名ID]{}".format(session)
        #     reply_message_to_group(self.client, f"{{\"text\":\"{title}\"}}", forward_response_data.message_id)