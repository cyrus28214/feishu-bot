from pydantic import BaseModel, Field, ValidationError, field_validator
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
    log_level: LogLevel = Field(default=LogLevel.INFO, description="日志级别")
    chat_id: str = Field(..., description="要匿名发送到的大群的chat_id")
    lark: LarkConfig = Field(..., description="飞书配置")

    @field_validator('log_level', mode='before')
    @classmethod
    def parse_log_level(cls, v):
        if isinstance(v, str):
            try:
                return LogLevel[v.upper()]
            except KeyError:
                raise ValueError(f'无效的日志级别: {v}。可用选项: {", ".join(LogLevel.__members__.keys())}')
        return v

    @classmethod
    def load(cls, config_path: str) -> "Config":
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