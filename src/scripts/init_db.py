#!/usr/bin/env python3
"""
資料庫初始化腳本
用於建立資料庫表格與欄位

使用方法：
    python3 src/scripts/init_db.py
"""

import os
import sys
from pathlib import Path

# 將專案根目錄加入 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from dotenv import load_dotenv
import mariadb
from werkzeug.security import generate_password_hash
from utils.debug import INFO_PRINT, ERROR_PRINT, WARN_PRINT

# 載入環境變數
env_path = project_root / "ENV" / ".env"
load_dotenv(env_path)


def get_db_config():
    """取得資料庫連線設定"""
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "app_db"),
    }


def create_database_if_not_exists():
    """建立資料庫（如果不存在）"""
    config = get_db_config()
    db_name = config.pop("database")
    
    try:
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        
        # 檢查資料庫是否存在
        cursor.execute("SHOW DATABASES LIKE ?", (db_name,))
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            INFO_PRINT(f"[OK] 已建立資料庫: {db_name}")
        else:
            INFO_PRINT(f"[INFO] 資料庫已存在: {db_name}")
        
        cursor.close()
        conn.close()
        return True
    except mariadb.Error as e:
        ERROR_PRINT(f"[ERROR] 建立資料庫時發生錯誤: {e}")
        return False


def init_tables():
    """初始化資料表"""
    config = get_db_config()
    
    try:
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        
        # 建立 users 資料表
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_users_table)
        INFO_PRINT("[OK] 已建立資料表: users")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mariadb.Error as e:
        ERROR_PRINT(f"[ERROR] 建立資料表時發生錯誤: {e}")
        return False


def create_default_user():
    """建立預設使用者（可選）"""
    config = get_db_config()
    
    try:
        conn = mariadb.connect(**config)
        cursor = conn.cursor(dictionary=True)
        
        # 檢查是否已有使用者
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            WARN_PRINT("[INFO] 資料表中已有使用者，跳過建立預設使用者")
            cursor.close()
            conn.close()
            return True
        
        # 建立預設使用者（從環境變數讀取）
        default_username = os.getenv("DEFAULT_USERNAME", "admin")
        default_password = os.getenv("DEFAULT_PASSWORD", "admin123")
        default_email = os.getenv("DEFAULT_EMAIL", "admin@example.com")
        
        if not default_username or not default_password:
            WARN_PRINT("[WARN] 未設定預設使用者帳號密碼，跳過建立預設使用者")
            cursor.close()
            conn.close()
            return True
        
        password_hash = generate_password_hash(default_password)
        
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (default_username, password_hash, default_email)
        )
        
        conn.commit()
        INFO_PRINT(f"[OK] 已建立預設使用者: {default_username}")
        if default_password == "admin123":
            WARN_PRINT("[WARN] 請在正式環境中更改預設使用者密碼！")
        
        cursor.close()
        conn.close()
        return True
    except mariadb.Error as e:
        ERROR_PRINT(f"[ERROR] 建立預設使用者時發生錯誤: {e}")
        return False


def main():
    """主函數"""
    INFO_PRINT("開始初始化資料庫...")
    
    # 檢查 MariaDB 驅動
    try:
        import mariadb
    except ImportError:
        ERROR_PRINT("[ERROR] 尚未安裝 mariadb Python 驅動")
        ERROR_PRINT("請執行: pip install mariadb")
        sys.exit(1)
    
    # 建立資料庫
    if not create_database_if_not_exists():
        sys.exit(1)
    
    # 初始化資料表
    if not init_tables():
        sys.exit(1)
    
    # 詢問是否建立預設使用者
    create_default = os.getenv("CREATE_DEFAULT_USER", "0").lower() in ("1", "true", "yes")
    if create_default:
        create_default_user()
    else:
        INFO_PRINT("[INFO] 跳過建立預設使用者（設定 CREATE_DEFAULT_USER=1 可啟用）")
    
    INFO_PRINT("[OK] 資料庫初始化完成！")


if __name__ == "__main__":
    main()

