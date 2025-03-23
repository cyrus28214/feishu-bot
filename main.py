from config import Config
import lark_oapi as lark
from event import event_handler

def main():
    config = Config.load()
    # 飞书客户端
    client = lark.Client.builder()\
        .app_id(config.lark.app_id)\
        .app_secret(config.lark.app_secret)\
        .build()
    
    # 飞书 websocket 客户端，建立双工通道，接收飞书事件
    ws = lark.ws.Client(
        config.lark.app_id,
        config.lark.app_secret,
        event_handler=event_handler,
        log_level=config.log_level
    )
    ws.start()

if __name__ == "__main__":
    main()
