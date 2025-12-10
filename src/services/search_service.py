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
        # 載入範例餐廳資料
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
        
        # 價格篩選
        if criteria.max_price is not None:
            filtered_results = []
            for restaurant in results:
                # 檢查餐廳是否有符合價格的菜單項目
                has_affordable_item = any(
                    item.price <= criteria.max_price
                    for item in restaurant.menu_items
                )
                if has_affordable_item:
                    filtered_results.append(restaurant)
            results = filtered_results
        
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
            # 根據最低價格排序
            results.sort(key=lambda r: min(item.price for item in r.menu_items) if r.menu_items else float('inf'))
        # 'distance' 排序需要位置資訊，暫時不實作
        
        return results

