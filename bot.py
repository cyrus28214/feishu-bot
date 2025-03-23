from config import Config
import lark_oapi as lark
from message import send_message_to_group
import json

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

        content = json.loads(event.event.message.content)
        message_type = event.event.message.message_type

        lark.logger.info(f"Received message: {content}")

        match message_type:
            case "text":
                send_message_to_group(self.client, self.config.chat_id, content["text"])
            case _:
                lark.logger.warning(f"Unsupported message type: {message_type}")

    def start(self):
        self.ws.start()