"""
Home 模組的路由定義
"""

from flask import render_template
from . import home_bp


@home_bp.route('/')
def index():
    """首頁"""
    return render_template('index.html')

