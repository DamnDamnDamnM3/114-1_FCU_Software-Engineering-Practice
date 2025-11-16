"""
Flask 主應用程式
自動載入所有模組的 Blueprint
"""

from flask import Flask
import os
import importlib


def create_app():
    """創建並配置 Flask 應用程式"""
    app = Flask(__name__)

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
                    print(f"✓ 已載入模組: {module_name}")
                else:
                    print(f"⚠ 模組 {module_name} 未找到 Blueprint ({blueprint_name})")
            except Exception as e:
                print(f"✗ 載入模組 {module_name} 時發生錯誤: {str(e)}")


# 創建應用程式實例
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
