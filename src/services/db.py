"""資料庫工具：提供 MariaDB 連線與通用查詢函式"""
from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

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
    # 資料表欄位與 SQL 腳本一致：userID、hashedPassword
    query = """
        SELECT userID AS id, username, hashedPassword
        FROM users
        WHERE username = ?
        LIMIT 1
    """

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (username,))
        record = cursor.fetchone()
        cursor.close()

    if not record:
        return None

    password_hash = record.get("hashedPassword")
    if password_hash and check_password_hash(password_hash, password):
        return {"id": record["id"], "username": record["username"]}

    return None


# ==================== 通用查詢函式 ====================

def fetch_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """執行查詢並返回所有結果（字典列表）"""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
    return results if results else []


def fetch_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """執行查詢並返回單一結果（字典）"""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
    return result


def execute(query: str, params: tuple = ()) -> int:
    """執行 INSERT/UPDATE/DELETE 並返回影響的行數"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
    return affected


def execute_returning_id(query: str, params: tuple = ()) -> int:
    """執行 INSERT 並返回新插入的 ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
    return last_id
