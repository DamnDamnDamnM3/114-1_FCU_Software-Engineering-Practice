"""
Frontend 模組
負責前端頁面的路由
"""

from flask import Blueprint

# 創建 Blueprint
frontend_bp = Blueprint('frontend', __name__, url_prefix='')

# 導入路由（必須在 Blueprint 創建之後）
from . import routes

