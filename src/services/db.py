"""資料庫工具：提供 MariaDB 連線與使用者驗證"""
from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional

from flask import current_app
from werkzeug.security import check_password_hash

try:
    import mariadb
except ImportError:  # pragma: no cover
    mariadb = None  # type: ignore


class DatabaseError(RuntimeError):
    """自訂例外"""


@dataclass
class User:
    id: int
    username: str


def driver_available() -> bool:
    """確認驅動是否安裝"""
    return mariadb is not None


def _get_db_config() -> Dict[str, Any]:
    defaults = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "app_db"),
    }

    try:
        app_config = current_app.config.get("DB_CONFIG", {})  # type: ignore[attr-defined]
    except RuntimeError:
        app_config = {}

    return {**defaults, **{k: v for k, v in app_config.items() if v}}


@contextmanager
def get_connection():
    """取得資料庫連線（自動關閉）"""
    if not driver_available():
        raise DatabaseError("尚未安裝 mariadb Python 驅動")

    config = _get_db_config()
    conn = None
    try:
        conn = mariadb.connect(**config)
        yield conn
    except mariadb.Error as exc:  # type: ignore[union-attr]
        raise DatabaseError(str(exc)) from exc
    finally:
        if conn:
            conn.close()


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """驗證使用者帳密，使用參數化查詢避免 SQL injection"""
    query = "SELECT id, username, password_hash FROM users WHERE username = ? LIMIT 1"

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (username,))
        record = cursor.fetchone()
        cursor.close()

    if not record:
        return None

    password_hash = record.get("password_hash")
    if password_hash and check_password_hash(password_hash, password):
        return {"id": record["id"], "username": record["username"]}

    return None
