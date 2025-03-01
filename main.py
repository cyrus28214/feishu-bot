from config import Config
from feishu import Feishu

def main():
    config = Config.load()
    feishu = Feishu(config.feishu)
    feishu.send_message({
        "msg_type": "text",
        "content": {
            "text": "Hello, world!"
        }
    })

if __name__ == "__main__":
    main()
