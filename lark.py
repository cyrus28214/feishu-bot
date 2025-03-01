import requests
import time
from config import LarkConfig
from typing import Optional
from dataclasses import dataclass

@dataclass
class Token:
    token: str
    expiry_time: float

class Lark:
    def __init__(self, config: LarkConfig):
        self.config = config
        self.session = requests.Session()
        self.token: Optional[Token] = None

    def get_token(self) -> Token:
        """直接调用API获取新的 tenant_access_token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret
        }

        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if data["code"] != 0:
                raise Exception(f"Failed to get tenant_access_token: {data}")

            return Token(
                token=data["tenant_access_token"],
                expiry_time=time.time() + float(data["expire"])
            )
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def refresh_token(self):
        buffer_time = 30 * 60 # 30分钟缓冲时间
        if self.token and self.token.expiry_time - time.time() > buffer_time:
            return
        self.token = self.get_token()
