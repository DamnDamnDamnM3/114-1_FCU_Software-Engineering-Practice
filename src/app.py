"""
Flask 主應用程式
自動載入所有模組的 Blueprint
"""

from flask import Flask
import os
import importlib
from dotenv import load_dotenv
from utils.debug import DEBUG_PRINT, WARN_PRINT, ERROR_PRINT, INFO_PRINT

# 載入 ENV/.env 檔案
env_path = os.path.join(os.path.dirname(__file__), "..", "ENV", ".env")
load_dotenv(env_path)


def create_app():
    """創建並配置 Flask 應用程式"""
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-key"),
        DB_CONFIG={
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            # SQL 腳本使用的資料庫名稱為 data，預設值與之對齊
            "database": os.getenv("DB_NAME", "data"),
        },
    )

    # 載入所有模組
    register_blueprints(app)

    return app


def register_blueprints(app):
    """
    自動註冊所有模組的 Blueprint

    此函數會掃描 modules 資料夾，自動載入所有模組的 Blueprint
    每個模組應該在 __init__.py 中導出一個 Blueprint 物件
    命名規則：{模組名}_bp
    """
    modules_path = os.path.join(os.path.dirname(__file__), "modules")

    # 遍歷 modules 資料夾中的所有子資料夾
    for module_name in os.listdir(modules_path):
        module_path = os.path.join(modules_path, module_name)

        # 只處理資料夾且不是 __pycache__
        if os.path.isdir(module_path) and not module_name.startswith("__"):
            try:
                # 動態導入模組
                module = importlib.import_module(f"modules.{module_name}")

                # 查找 Blueprint（命名規則：{模組名}_bp）
                blueprint_name = f"{module_name}_bp"
                if hasattr(module, blueprint_name):
                    blueprint = getattr(module, blueprint_name)
                    app.register_blueprint(blueprint)
                    INFO_PRINT(f"[OK] 已載入模組: {module_name}")
                else:
                    WARN_PRINT(f"[WARN] 模組 {module_name} 未找到 Blueprint ({blueprint_name})")
            except Exception as e:
                ERROR_PRINT(f"[ERROR] 載入模組 {module_name} 時發生錯誤: {str(e)}")


# 創建應用程式實例
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
