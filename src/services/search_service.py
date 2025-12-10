"""
搜尋服務
"""

from typing import List
from models.filter_criteria import FilterCriteria
from data.sample_data import Restaurant, SampleData


class SearchService:
    """餐廳搜尋服務"""
    
    def __init__(self):
        """初始化搜尋服務"""
        # 載入餐廳資料（從 CSV）
        self._restaurants = SampleData.create_sample_restaurants()
    
    def reload_data(self):
        """重新載入資料"""
        SampleData.clear_cache()
        self._restaurants = SampleData.create_sample_restaurants()
    
    def search_restaurants(self, criteria: FilterCriteria) -> List[Restaurant]:
        """
        根據條件搜尋餐廳
        
        Args:
            criteria: 篩選條件
            
        Returns:
            符合條件的餐廳列表
        """
        results = self._restaurants.copy()
        
        # 關鍵字搜尋
        if criteria.keyword:
            keyword_lower = criteria.keyword.lower()
            results = [
                r for r in results
                if keyword_lower in r.name.lower() or
                   keyword_lower in r.address.lower() or
                   any(keyword_lower in item.name.lower() for item in r.menu_items)
            ]
        
        # 類別篩選
        if criteria.categories:
            results = [
                r for r in results
                if r.food_type in criteria.categories
            ]
        
        # 素食篩選
        if criteria.vegetarian:
            results = [
                r for r in results
                if r.vegetarian_option in ['蛋奶素', '全素']
            ]
        
        # 價格篩選（精確匹配 price_range）
        if criteria.max_price is not None:
            # max_price 對應 price_range: 200->1, 400->2, 600->3
            if criteria.max_price <= 200:
                target_range = 1
            elif criteria.max_price <= 400:
                target_range = 2
            elif criteria.max_price <= 600:
                target_range = 3
            else:
                target_range = None  # $$$$ 顯示所有
            
            if target_range is not None:
                results = [
                    r for r in results
                    if r.price_range == target_range  # 精確匹配
                ]
        
        # 評分篩選
        if criteria.min_rating is not None:
            results = [
                r for r in results
                if r.average_rating >= criteria.min_rating
            ]
        
        # 排序
        if criteria.sort_by == 'rating':
            results.sort(key=lambda r: r.average_rating, reverse=True)
        elif criteria.sort_by == 'price':
            results.sort(key=lambda r: r.price_range)
        # 'distance' 排序需要位置資訊，暫時不實作
        
        return results

