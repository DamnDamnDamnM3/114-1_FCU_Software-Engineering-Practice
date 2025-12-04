"""
MenuItem 類別
菜單項目
"""

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from .nutrition_info import NutritionInfo

if TYPE_CHECKING:
    from .restaurant import Restaurant


@dataclass
class MenuItem:
    """菜單項目"""
    item_id: str
    name: str
    description: str
    price: float
    nutrition_info: Optional[NutritionInfo] = None
    restaurant: Optional['Restaurant'] = None

    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        price: float,
        nutrition_info: Optional[NutritionInfo] = None
    ):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price
        self.nutrition_info = nutrition_info
        self.restaurant = None

    def get_nutrition_info(self) -> Optional[NutritionInfo]:
        """
        取得營養資訊
        
        Returns:
            NutritionInfo: 營養資訊，如果不存在則返回 None
        """
        return self.nutrition_info
