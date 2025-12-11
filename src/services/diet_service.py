"""
飲食記錄資料庫服務
處理用戶的飲食記錄 CRUD
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from services.db import fetch_all, fetch_one, execute, execute_returning_id, driver_available, DatabaseError


@dataclass
class DietLog:
    """飲食記錄"""
    log_id: int
    user_id: int
    item_id: int
    timestamp: datetime
    portion_size: float = 1.0
    
    # 額外資訊（從 JOIN 查詢取得）
    item_name: str = ""
    restaurant_name: str = ""
    calories: int = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0


class DietService:
    """飲食記錄服務"""
    
    @staticmethod
    def add_diet_log(user_id: int, item_id: int, portion_size: float = 1.0, timestamp: Optional[str] = None) -> Optional[int]:
        """
        新增飲食記錄
        
        Args:
            user_id: 使用者 ID
            item_id: 菜單項目 ID
            portion_size: 份量倍數（預設 1.0）
            timestamp: 進食時間 (ISO 格式字串)，若為 None 則使用當前時間
            
        Returns:
            新記錄的 ID，失敗則返回 None
        """
        if not driver_available():
            print("[ERROR] 資料庫驅動不可用")
            return None
        
        try:
            if timestamp:
                query = """
                    INSERT INTO diet_logs (userID, itemID, timestamp, portionSize)
                    VALUES (?, ?, ?, ?)
                """
                log_id = execute_returning_id(query, (user_id, item_id, timestamp, portion_size))
            else:
                query = """
                    INSERT INTO diet_logs (userID, itemID, timestamp, portionSize)
                    VALUES (?, ?, NOW(), ?)
                """
                log_id = execute_returning_id(query, (user_id, item_id, portion_size))
            return log_id
            
        except DatabaseError as e:
            print(f"[ERROR] 新增飲食記錄失敗: {e}")
            return None
    
    @staticmethod
    def get_user_diet_logs(user_id: int, limit: int = 50) -> List[DietLog]:
        """
        取得使用者的飲食記錄
        
        Args:
            user_id: 使用者 ID
            limit: 最多返回筆數
            
        Returns:
            飲食記錄列表
        """
        if not driver_available():
            return []
        
        try:
            query = """
                SELECT d.logID, d.userID, d.itemID, d.timestamp, d.portionSize,
                       m.name as itemName, r.name as restaurantName,
                       m.calories, m.protein, m.carbs, m.fat
                FROM diet_logs d
                JOIN menu_items m ON d.itemID = m.itemID
                JOIN restaurants r ON m.restaurantID = r.restaurantID
                WHERE d.userID = ?
                ORDER BY d.timestamp DESC
                LIMIT ?
            """
            rows = fetch_all(query, (user_id, limit))
            
            logs = []
            for row in rows:
                log = DietLog(
                    log_id=row['logID'],
                    user_id=row['userID'],
                    item_id=row['itemID'],
                    timestamp=row['timestamp'],
                    portion_size=float(row['portionSize'] or 1.0),
                    item_name=row['itemName'] or '',
                    restaurant_name=row['restaurantName'] or '',
                    calories=int(row['calories'] or 0),
                    protein=float(row['protein'] or 0),
                    carbs=float(row['carbs'] or 0),
                    fat=float(row['fat'] or 0)
                )
                logs.append(log)
            
            return logs
            
        except DatabaseError as e:
            print(f"[ERROR] 讀取飲食記錄失敗: {e}")
            return []

    @staticmethod
    def get_date_diet_logs(user_id: int, date_str: str) -> List[DietLog]:
        """
        取得使用者指定日期的飲食記錄
        
        Args:
            user_id: 使用者 ID
            date_str: 日期字串 (YYYY-MM-DD)
            
        Returns:
            該日飲食記錄列表
        """
        if not driver_available():
            return []
        
        try:
            query = """
                SELECT d.logID, d.userID, d.itemID, d.timestamp, d.portionSize,
                       m.name as itemName, r.name as restaurantName,
                       m.calories, m.protein, m.carbs, m.fat
                FROM diet_logs d
                JOIN menu_items m ON d.itemID = m.itemID
                JOIN restaurants r ON m.restaurantID = r.restaurantID
                WHERE d.userID = ? AND DATE(d.timestamp) = ?
                ORDER BY d.timestamp DESC
            """
            rows = fetch_all(query, (user_id, date_str))
            
            logs = []
            for row in rows:
                log = DietLog(
                    log_id=row['logID'],
                    user_id=row['userID'],
                    item_id=row['itemID'],
                    timestamp=row['timestamp'],
                    portion_size=float(row['portionSize'] or 1.0),
                    item_name=row['itemName'] or '',
                    restaurant_name=row['restaurantName'] or '',
                    calories=int(row['calories'] or 0),
                    protein=float(row['protein'] or 0),
                    carbs=float(row['carbs'] or 0),
                    fat=float(row['fat'] or 0)
                )
                logs.append(log)
            
            return logs
            
        except DatabaseError as e:
            print(f"[ERROR] 讀取飲食記錄失敗: {e}")
            return []
    
    @staticmethod
    def get_today_diet_logs(user_id: int) -> List[DietLog]:
        """
        取得使用者今日的飲食記錄
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            今日飲食記錄列表
        """
        if not driver_available():
            return []
        
        try:
            query = """
                SELECT d.logID, d.userID, d.itemID, d.timestamp, d.portionSize,
                       m.name as itemName, r.name as restaurantName,
                       m.calories, m.protein, m.carbs, m.fat
                FROM diet_logs d
                JOIN menu_items m ON d.itemID = m.itemID
                JOIN restaurants r ON m.restaurantID = r.restaurantID
                WHERE d.userID = ? AND DATE(d.timestamp) = CURDATE()
                ORDER BY d.timestamp DESC
            """
            rows = fetch_all(query, (user_id,))
            
            logs = []
            for row in rows:
                log = DietLog(
                    log_id=row['logID'],
                    user_id=row['userID'],
                    item_id=row['itemID'],
                    timestamp=row['timestamp'],
                    portion_size=float(row['portionSize'] or 1.0),
                    item_name=row['itemName'] or '',
                    restaurant_name=row['restaurantName'] or '',
                    calories=int(row['calories'] or 0),
                    protein=float(row['protein'] or 0),
                    carbs=float(row['carbs'] or 0),
                    fat=float(row['fat'] or 0)
                )
                logs.append(log)
            
            return logs
            
        except DatabaseError as e:
            print(f"[ERROR] 讀取今日飲食記錄失敗: {e}")
            return []
    
    @staticmethod
    def get_today_nutrition_summary(user_id: int) -> Dict[str, float]:
        """
        取得使用者今日營養攝取總計
        
        Args:
            user_id: 使用者 ID
            
        Returns:
            營養攝取總計 dict
        """
        if not driver_available():
            return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        try:
            query = """
                SELECT 
                    COALESCE(SUM(m.calories * d.portionSize), 0) as totalCalories,
                    COALESCE(SUM(m.protein * d.portionSize), 0) as totalProtein,
                    COALESCE(SUM(m.carbs * d.portionSize), 0) as totalCarbs,
                    COALESCE(SUM(m.fat * d.portionSize), 0) as totalFat
                FROM diet_logs d
                JOIN menu_items m ON d.itemID = m.itemID
                WHERE d.userID = ? AND DATE(d.timestamp) = CURDATE()
            """
            row = fetch_one(query, (user_id,))
            
            if row:
                return {
                    'calories': float(row['totalCalories'] or 0),
                    'protein': float(row['totalProtein'] or 0),
                    'carbs': float(row['totalCarbs'] or 0),
                    'fat': float(row['totalFat'] or 0)
                }
            
            return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            
        except DatabaseError as e:
            print(f"[ERROR] 計算今日營養攝取失敗: {e}")
            return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    
    @staticmethod
    def delete_diet_log(log_id: int, user_id: int) -> bool:
        """
        刪除飲食記錄（需驗證擁有者）
        
        Args:
            log_id: 記錄 ID
            user_id: 使用者 ID（用於驗證）
            
        Returns:
            是否刪除成功
        """
        if not driver_available():
            return False
        
        try:
            # 確保只能刪除自己的記錄
            query = """
                DELETE FROM diet_logs
                WHERE logID = ? AND userID = ?
            """
            affected = execute(query, (log_id, user_id))
            return affected > 0
            
        except DatabaseError as e:
            print(f"[ERROR] 刪除飲食記錄失敗: {e}")
            return False
    
    @staticmethod
    def update_portion_size(log_id: int, user_id: int, portion_size: float) -> bool:
        """
        更新份量
        
        Args:
            log_id: 記錄 ID
            user_id: 使用者 ID（用於驗證）
            portion_size: 新的份量
            
        Returns:
            是否更新成功
        """
        if not driver_available():
            return False
        
        try:
            query = """
                UPDATE diet_logs
                SET portionSize = ?
                WHERE logID = ? AND userID = ?
            """
            affected = execute(query, (portion_size, log_id, user_id))
            return affected > 0
            
        except DatabaseError as e:
            print(f"[ERROR] 更新飲食記錄失敗: {e}")
            return False
