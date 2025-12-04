"""
Restaurant 模組
處理餐廳搜尋、推薦、飲食記錄和分析相關路由
"""

from flask import Blueprint

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurants")

from . import routes


