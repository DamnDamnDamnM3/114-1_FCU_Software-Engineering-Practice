"""
範例資料生成器
"""

from typing import List
from dataclasses import dataclass


@dataclass
class MenuItem:
    """菜單項目"""
    name: str
    price: float
    description: str = ""


@dataclass
class Restaurant:
    """餐廳資料"""
    restaurant_id: str
    name: str
    address: str
    average_rating: float
    menu_items: List[MenuItem]
    food_type: str = ""


class SampleData:
    """範例資料生成器"""
    
    @staticmethod
    def create_sample_restaurants() -> List[Restaurant]:
        """建立範例餐廳資料"""
        restaurants = []
        
        # 建立一些範例餐廳
        sample_restaurants = [
            {
                "restaurant_id": "rest_001",
                "name": "海鹽慢食",
                "address": "台中市西屯區台灣大道三段99號",
                "average_rating": 4.5,
                "food_type": "台式",
                "menu_items": [
                    MenuItem("招牌滷肉飯", 45.0, "傳統滷肉飯"),
                    MenuItem("燙青菜", 40.0, "時令青菜"),
                    MenuItem("貢丸湯", 35.0, "手工貢丸湯")
                ]
            },
            {
                "restaurant_id": "rest_002",
                "name": "ㄧ魂拉麵",
                "address": "台中市西屯區逢甲路20號",
                "average_rating": 4.3,
                "food_type": "日式",
                "menu_items": [
                    MenuItem("豚骨拉麵", 180.0, "濃郁豚骨湯頭"),
                    MenuItem("炸豬排定食", 200.0, "日式炸豬排"),
                    MenuItem("鮭魚丼", 250.0, "新鮮鮭魚丼飯")
                ]
            },
            {
                "restaurant_id": "rest_003",
                "name": "Luigi義大利麵",
                "address": "台中市西屯區文華路100號",
                "average_rating": 4.2,
                "food_type": "義式",
                "menu_items": [
                    MenuItem("白醬培根麵", 190.0, "濃郁白醬義大利麵"),
                    MenuItem("瑪格麗特披薩", 220.0, "經典義式披薩"),
                    MenuItem("凱薩沙拉", 150.0, "新鮮蔬菜沙拉")
                ]
            },
            {
                "restaurant_id": "rest_004",
                "name": "肌肉海灘餐盒",
                "address": "台中市西屯區福星路50號",
                "average_rating": 4.6,
                "food_type": "健康餐",
                "menu_items": [
                    MenuItem("舒肥雞胸餐盒", 130.0, "低脂高蛋白"),
                    MenuItem("香煎鮭魚飯", 160.0, "富含Omega-3"),
                    MenuItem("無糖豆漿", 25.0, "高蛋白飲品")
                ]
            },
            {
                "restaurant_id": "rest_005",
                "name": "歐巴炸雞",
                "address": "台中市西屯區西安街30號",
                "average_rating": 4.4,
                "food_type": "韓式",
                "menu_items": [
                    MenuItem("韓式炸雞", 220.0, "韓式風味炸雞"),
                    MenuItem("泡菜豆腐鍋", 160.0, "韓式泡菜鍋"),
                    MenuItem("石鍋拌飯", 180.0, "經典韓式拌飯")
                ]
            }
        ]
        
        for data in sample_restaurants:
            restaurant = Restaurant(
                restaurant_id=data["restaurant_id"],
                name=data["name"],
                address=data["address"],
                average_rating=data["average_rating"],
                food_type=data["food_type"],
                menu_items=data["menu_items"]
            )
            restaurants.append(restaurant)
        
        return restaurants

