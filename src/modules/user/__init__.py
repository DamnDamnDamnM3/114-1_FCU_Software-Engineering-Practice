"""
User 模組：處理登入等使用者驗證相關路由
"""

from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/auth")

from . import routes
