"""
Home 模組
負責首頁和關於頁面的路由
"""

from flask import Blueprint

# 創建 Blueprint，url_prefix 是可選的，用於為所有路由添加前綴
home_bp = Blueprint('home', __name__, url_prefix='')

# 導入路由（必須在 Blueprint 創建之後）
from . import routes

