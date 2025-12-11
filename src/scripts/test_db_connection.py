#!/usr/bin/env python3
"""
資料庫連線測試腳本
用於測試資料庫連線是否正常

使用方法：
    python3 src/scripts/test_db_connection.py
"""

import os
import sys
from pathlib import Path

# 將專案根目錄加入 Python 路徑
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from dotenv import load_dotenv
import mariadb
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


def test_connection():
    """測試資料庫連線"""
    INFO_PRINT("開始測試資料庫連線...")
    
    # 檢查 MariaDB 驅動
    try:
        import mariadb
    except ImportError:
        ERROR_PRINT("[ERROR] 尚未安裝 mariadb Python 驅動")
        ERROR_PRINT("請執行: pip install mariadb")
        return False
    
    config = get_db_config()
    
    INFO_PRINT(f"[INFO] 連線設定:")
    INFO_PRINT(f"  - Host: {config['host']}")
    INFO_PRINT(f"  - Port: {config['port']}")
    INFO_PRINT(f"  - User: {config['user']}")
    INFO_PRINT(f"  - Database: {config['database']}")
    
    # 測試連線（不指定資料庫）
    try:
        config_no_db = config.copy()
        db_name = config_no_db.pop("database")
        
        INFO_PRINT(f"\n[測試 1] 連線到 MariaDB 伺服器...")
        conn = mariadb.connect(**config_no_db)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        INFO_PRINT(f"[OK] 成功連線到 MariaDB 伺服器")
        INFO_PRINT(f"[INFO] MariaDB 版本: {version}")
        cursor.close()
        conn.close()
    except mariadb.Error as e:
        ERROR_PRINT(f"[ERROR] 無法連線到 MariaDB 伺服器: {e}")
        ERROR_PRINT("[提示] 請檢查：")
        ERROR_PRINT("  1. MariaDB 服務是否正在運行")
        ERROR_PRINT("  2. 連線設定（host, port, user, password）是否正確")
        ERROR_PRINT("  3. 防火牆設定是否允許連線")
        return False
    
    # 測試連線到指定資料庫
    try:
        INFO_PRINT(f"\n[測試 2] 連線到資料庫 '{db_name}'...")
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        
        # 檢查資料庫是否存在
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        INFO_PRINT(f"[OK] 成功連線到資料庫: {current_db}")
        
        # 檢查資料表是否存在
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            INFO_PRINT(f"[OK] 資料庫中有 {len(tables)} 個資料表:")
            for table in tables:
                INFO_PRINT(f"  - {table[0]}")
        else:
            WARN_PRINT("[WARN] 資料庫中沒有資料表")
            WARN_PRINT("[提示] 請執行初始化腳本: python3 src/scripts/init_db.py")
        
        cursor.close()
        conn.close()
        
        INFO_PRINT(f"\n[OK] 資料庫連線測試完成！")
        return True
        
    except mariadb.Error as e:
        error_msg = str(e)
        if "Unknown database" in error_msg:
            ERROR_PRINT(f"[ERROR] 資料庫 '{db_name}' 不存在")
            ERROR_PRINT(f"[提示] 請執行初始化腳本建立資料庫: python3 src/scripts/init_db.py")
        else:
            ERROR_PRINT(f"[ERROR] 無法連線到資料庫: {e}")
        return False


def main():
    """主函數"""
    success = test_connection()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

