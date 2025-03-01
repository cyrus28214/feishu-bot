from pydantic import BaseModel, Field, ValidationError
import toml

class LarkConfig(BaseModel):
    app_id: str = Field(..., description="飞书app id")
    app_secret: str = Field(..., description="飞书app secret")

class Config(BaseModel):
    lark: LarkConfig = Field(..., description="飞书配置")

    @classmethod
    def load(cls, config_path: str = "config.toml") -> "Config":
        try:
            config_dict = toml.load(config_path)
            return cls(**config_dict)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {config_path} 不存在")
        except toml.TomlDecodeError as e:
            raise ValueError(f"配置文件 {config_path} 格式错误: {e}")
        except ValidationError as e:
            raise ValueError(f"配置文件 {config_path} 验证失败: {e}")