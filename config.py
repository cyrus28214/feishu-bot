from pydantic import BaseModel, Field, ValidationError
import tomllib
from enum import Enum

class LarkConfig(BaseModel):
    app_id: str = Field(..., description="飞书app id")
    app_secret: str = Field(..., description="飞书app secret")

# copied from lark_oapi/core/enum.py
class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class Config(BaseModel):
    lark: LarkConfig = Field(..., description="飞书配置")
    log_level: LogLevel = Field(description="日志级别", default=LogLevel.INFO)
    chat_id: str = Field(..., description="转发群聊id")
    chat_type: str = Field(..., description="转发群聊类型")

    @classmethod
    def load(cls, config_path: str = "config.toml") -> "Config":
        try:
            with open(config_path, "rb") as f:
                config_dict = tomllib.load(f)
            return cls(**config_dict)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {config_path} 不存在")
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"配置文件 {config_path} 格式错误: {e}")
        except ValidationError as e:
            raise ValueError(f"配置文件 {config_path} 验证失败: {e}")