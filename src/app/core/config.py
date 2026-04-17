import os

# 从 pydantic_settings 包导入 BaseSettings 类和 SettingsConfigDict 类
# BaseSettings: Pydantic 提供的配置管理基类，能自动读取 .env 文件和环境变量
# SettingsConfigDict: Pydantic V2 中用来配置 Settings 行为的配置字典类型
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
        项目配置类
        继承 BaseSettings 后，会自动按以下优先级读取配置：
        1. 系统环境变量（最高优先级）
        2. .env 文件（中等优先级）
        3. 类属性中定义的默认值（最低优先级）
    """
    # ========== Pydantic V2 的配置方式 ==========
    # 使用 model_config 属性，值是 SettingsConfigDict 实例
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # ========== 数据库连接配置项 ==========
    # 每个属性的格式：属性名: 类型注解 = 默认值
    # 注意：属性名必须全大写，才能自动匹配同名的环境变量
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    # 密码不从 .env 文件读取，而是直接从系统环境变量读取
    # os.getenv("MYSQL_PASSWORD", "") 的含义：
    #   读取系统环境变量 MYSQL_PASSWORD 的值
    #   如果不存在该环境变量，则返回空字符串 ""
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = "db_course_select"

    # ========== 计算属性 ==========
    # @property 装饰器：让这个方法可以像属性一样被访问（settings.DATABASE_URL，不需要加括号）
    # 这个方法不会被 .env 文件或环境变量覆盖，因为它的值是由其他配置项动态计算出来的
    @property
    def DATABASE_URL(self) -> str:
        """
           根据上面的配置项，动态拼接出完整的数据库连接 URL
           返回值示例：
           mysql+pymysql://root:123456@localhost:3306/fastapi_kb_demo?charset=utf8mb4
           格式说明：
           mysql+pymysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
        """
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset=utf8mb4"
        )


# 创建全局配置实例，供项目其他模块导入使用
# 其他文件通过 from app.core.config import settings 就能获取这个实例
settings = Settings()

