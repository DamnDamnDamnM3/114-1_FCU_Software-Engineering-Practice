from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from services.db import execute_returning_id, fetch_one, execute

class UserService:
    def create_user(self, username: str, password: str, mode: str = 'NORMAL', 
                    budget: float = 0, target_calories: int = None, 
                    target_protein: float = None, target_fat: float = None) -> Optional[int]:
        """
        註冊新使用者
        :return: 新使用者的 ID，如果使用者名稱已存在則拋出異常或返回 None
        """
        # 檢查使用者名稱是否已存在
        # Use ? for mariadb placeholder
        existing_user = fetch_one("SELECT userID FROM users WHERE username = ?", (username,))
        if existing_user:
            raise ValueError("Username already exists")

        hashed_password = generate_password_hash(password)
        
        query = """
            INSERT INTO users (username, hashedPassword, mode, budget, targetCalories, targetProtein, targetFat)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (username, hashed_password, mode, budget, target_calories, target_protein, target_fat)
        
        user_id = execute_returning_id(query, params)
        return user_id

    def verify_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        驗證使用者登入
        :return: 使用者資料字典 (不含密碼)，驗證失敗返回 None
        """
        query = "SELECT * FROM users WHERE username = ?"
        user = fetch_one(query, (username,))
        
        if user and check_password_hash(user['hashedPassword'], password):
            # 移除密碼欄位再回傳
            user.pop('hashedPassword', None)
            return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        根據 ID 取得使用者資料
        """
        query = "SELECT * FROM users WHERE userID = ?"
        user = fetch_one(query, (user_id,))
        if user:
            user.pop('hashedPassword', None)
        return user
