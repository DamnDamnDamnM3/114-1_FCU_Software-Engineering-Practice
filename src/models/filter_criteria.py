"""
篩選條件資料模型
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class FilterCriteria:
    """餐廳搜尋篩選條件"""
    keyword: Optional[str] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    categories: List[str] = field(default_factory=list)  # 食物類別 (日式, 台式, etc.)
    vegetarian: bool = False  # 是否只顯示素食
    sort_by: str = 'rating'  # 'rating', 'price', 'distance'

