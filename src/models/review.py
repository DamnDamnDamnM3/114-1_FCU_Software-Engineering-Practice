"""
Review 類別
餐廳評論
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .restaurant import Restaurant


@dataclass
class Review:
    """餐廳評論"""
    review_id: str
    rating: int
    comment: str
    timestamp: datetime
    restaurant: Optional['Restaurant'] = None

    def __init__(
        self,
        review_id: str,
        rating: int,
        comment: str,
        timestamp: Optional[datetime] = None
    ):
        self.review_id = review_id
        self.rating = rating
        self.comment = comment
        self.timestamp = timestamp if timestamp else datetime.now()
        self.restaurant = None
