import requests
from config import FeishuConfig

class Feishu:
    def __init__(self, config: FeishuConfig):
        self.config = config

    def send_message(self, message: dict):
        requests.post(self.config.webhook_url, json=message)
