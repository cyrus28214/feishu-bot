from config import Config
import lark_oapi as lark

def main():
    config = Config.load()
    client = lark.Client.builder()\
        .app_id(config.lark.app_id)\
        .app_secret(config.lark.app_secret)\
        .build()

if __name__ == "__main__":
    main()
