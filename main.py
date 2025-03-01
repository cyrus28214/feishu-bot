from config import Config
from lark import Lark

def main():
    config = Config.load()
    lark = Lark(config.lark)
    
if __name__ == "__main__":
    main()
