"""
Home 模組的路由定義
"""

from flask import render_template
from . import home_bp


@home_bp.route('/')
def index():
    """首頁"""
    return render_template('home/index.html')


@home_bp.route('/about')
def about():
    """關於頁面"""
    return render_template('home/about.html')

