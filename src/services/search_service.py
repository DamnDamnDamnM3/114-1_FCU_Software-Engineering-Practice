"""
SearchService 類別
負責處理餐廳搜尋邏輯
"""

from typing import List
from models.restaurant import Restaurant
from models.filter_criteria import FilterCriteria


class SearchService:
    """餐廳搜尋服務"""

    def __init__(self):
        """初始化搜尋服務"""
        pass

    def search_restaurants(self, criteria: FilterCriteria) -> List[Restaurant]:
        """
        搜尋餐廳
        
        負責處理關鍵字搜尋、價格篩選、評分排序等邏輯。
        搜尋演算法先保留（TODO），但需建立方法與資料流程。
        
        Args:
            criteria: 篩選條件
        
        Returns:
            List[Restaurant]: 符合條件的餐廳列表
        """
        # TODO: implement search algorithm
        # 1. 根據關鍵字搜尋餐廳名稱、地址、描述
        # 2. 根據 max_price 篩選菜單項目價格
        # 3. 根據 min_rating 篩選餐廳評分
        # 4. 根據 sort_by 排序結果（price, rating, distance）
        # 5. 返回符合條件的餐廳列表
        
        return []
