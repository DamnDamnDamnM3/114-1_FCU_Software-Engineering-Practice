"""
Restaurant 類別
餐廳資料模型
"""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .menu_item import MenuItem
    from .review import Review
else:
    from .menu_item import MenuItem
    from .review import Review


@dataclass
class Restaurant:
    """餐廳"""
    restaurant_id: str
    name: str
    address: str
    latitude: float
    longitude: float
    google_map_link: str
    average_rating: float = 0.0
    menu_items: List['MenuItem'] = field(default_factory=list)
    reviews: List['Review'] = field(default_factory=list)

    def __init__(
        self,
        restaurant_id: str,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
        google_map_link: str,
        average_rating: float = 0.0
    ):
        self.restaurant_id = restaurant_id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.google_map_link = google_map_link
        self.average_rating = average_rating
        self.menu_items = []
        self.reviews = []

    def get_menu(self) -> List['MenuItem']:
        """
        取得菜單項目列表
        
        Returns:
            List[MenuItem]: 菜單項目列表
        """
        return self.menu_items

    def get_reviews(self) -> List['Review']:
        """
        取得評論列表
        
        Returns:
            List[Review]: 評論列表
        """
        return self.reviews

    def add_menu_item(self, menu_item: 'MenuItem') -> None:
        """新增菜單項目"""
        menu_item.restaurant = self
        self.menu_items.append(menu_item)

    def add_review(self, review: 'Review') -> None:
        """新增評論並更新平均評分"""
        review.restaurant = self
        self.reviews.append(review)
        self._update_average_rating()

    def _update_average_rating(self) -> None:
        """更新平均評分"""
        if not self.reviews:
            self.average_rating = 0.0
            return
        
        total_rating = sum(review.rating for review in self.reviews)
        self.average_rating = total_rating / len(self.reviews)
