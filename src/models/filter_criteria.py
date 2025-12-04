"""
FilterCriteria 類別
用於搜尋服務的篩選條件
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FilterCriteria:
    """搜尋篩選條件"""
    keyword: Optional[str] = None      # 關鍵字
    max_price: Optional[float] = None # 最高價格
    min_rating: Optional[float] = None # 最低評分
    sort_by: Optional[str] = None      # 排序方式（例如：price, rating, distance）

    def __init__(
        self,
        keyword: Optional[str] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        sort_by: Optional[str] = None
    ):
        self.keyword = keyword
        self.max_price = max_price
        self.min_rating = min_rating
        self.sort_by = sort_by
