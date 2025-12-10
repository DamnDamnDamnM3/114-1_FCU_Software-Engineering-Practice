"""
篩選條件資料模型
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FilterCriteria:
    """餐廳搜尋篩選條件"""
    keyword: Optional[str] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    sort_by: str = 'rating'  # 'rating', 'price', 'distance'

