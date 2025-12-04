"""
RecommendationService 類別
負責生成餐廳/菜單推薦
"""

from typing import List
from models.user import User
from models.menu_item import MenuItem


class RecommendationService:
    """推薦服務"""

    def __init__(self):
        """初始化推薦服務"""
        pass

    def get_recommendations(self, user: User) -> List[MenuItem]:
        """
        取得推薦菜單項目
        
        使用 UserProfile、HealthProfile、DietLog、NutritionInfo 資料生成推薦。
        推薦演算法先以 TODO 佔位，但 class 架構與流程要完整設計。
        需要具備資料收集、排序、過濾等處理的接口。
        
        Args:
            user: 使用者
        
        Returns:
            List[MenuItem]: 推薦的菜單項目列表
        """
        # TODO: implement recommendation algorithm
        # 1. 收集使用者資料：
        #    - UserProfile (budget, mode)
        #    - HealthProfile (target_calories, target_protein, target_fat) - 如果 mode = FITNESS
        #    - DietLogs (歷史飲食記錄)
        #    - NutritionInfo (營養資訊)
        #
        # 2. 根據模式選擇推薦策略：
        #    - NORMAL: 根據預算和評分推薦
        #    - FITNESS: 根據健康目標和營養需求推薦
        #    - TOURIST: 根據地理位置和熱門度推薦
        #
        # 3. 過濾和排序：
        #    - 過濾不符合預算的項目
        #    - 過濾不符合健康目標的項目（FITNESS 模式）
        #    - 根據相關性、評分、價格等排序
        #
        # 4. 返回推薦列表
        
        if not user.profile:
            return []
        
        recommendations = []
        
        # TODO: 實作推薦邏輯
        # 範例流程：
        # - 收集使用者偏好
        # - 分析歷史記錄
        # - 生成候選項目
        # - 過濾和排序
        # - 返回結果
        
        return recommendations
