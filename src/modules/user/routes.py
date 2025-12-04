"""
User 模組路由
"""

from flask import render_template, request, redirect, url_for, flash
from services.db import authenticate_user, DatabaseError, driver_available
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """顯示並處理登入表單"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("請輸入帳號與密碼", "warning")
        else:
            try:
                user = authenticate_user(username=username, password=password)
                if user:
                    flash(f"歡迎回來，{user['username']}！", "success")
                    return redirect(url_for("home.index"))
                flash("帳號或密碼不正確", "danger")
            except DatabaseError as exc:
                flash(f"登入服務暫時無法使用：{exc}", "danger")

    return render_template(
        "user/login.html",
        driver_ready=driver_available(),
    )
