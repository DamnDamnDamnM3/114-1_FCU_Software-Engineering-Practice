"""
SampleData 類別
提供範例資料用於測試和開發
"""

from typing import List
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.nutrition_info import NutritionInfo
from models.review import Review
from models.user import User
from models.user_profile import UserProfile
from models.app_mode import AppMode
from models.health_profile import HealthProfile
from datetime import datetime


class SampleData:
    """範例資料生成器"""

    @staticmethod
    def create_sample_restaurants() -> List[Restaurant]:
        """建立範例餐廳資料"""
        restaurants = []
        
        # 餐廳 1
        restaurant1 = Restaurant(
            restaurant_id="rest_001",
            name="海鹽慢食",
            address="台中市西屯區台灣大道三段99號",
            latitude=24.1794,
            longitude=120.6444,
            google_map_link="https://maps.google.com/?q=24.1794,120.6444",
            average_rating=4.5
        )
        
        # 餐廳 1 的菜單
        menu_item1_1 = MenuItem(
            item_id="item_001",
            name="地中海沙拉",
            description="結合地中海香氣與在地蔬果，主打健康無負擔料理",
            price=280.0,
            nutrition_info=NutritionInfo(calories=350, protein=12.0, carbs=25.0, fat=18.0)
        )
        menu_item1_2 = MenuItem(
            item_id="item_002",
            name="香草烤雞",
            description="使用新鮮香草醃製，低溫慢烤",
            price=420.0,
            nutrition_info=NutritionInfo(calories=520, protein=45.0, carbs=8.0, fat=28.0)
        )
        restaurant1.add_menu_item(menu_item1_1)
        restaurant1.add_menu_item(menu_item1_2)
        
        # 餐廳 1 的評論
        review1_1 = Review(
            review_id="rev_001",
            rating=5,
            comment="非常健康的選擇，食材新鮮",
            timestamp=datetime.now()
        )
        review1_2 = Review(
            review_id="rev_002",
            rating=4,
            comment="價格稍高但值得",
            timestamp=datetime.now()
        )
        restaurant1.add_review(review1_1)
        restaurant1.add_review(review1_2)
        
        restaurants.append(restaurant1)
        
        # 餐廳 2
        restaurant2 = Restaurant(
            restaurant_id="rest_002",
            name="暮色和牛所",
            address="台中市北區三民路三段161號",
            latitude=24.1500,
            longitude=120.6800,
            google_map_link="https://maps.google.com/?q=24.1500,120.6800",
            average_rating=4.8
        )
        
        menu_item2_1 = MenuItem(
            item_id="item_003",
            name="60日熟成牛排",
            description="主打 60 日熟成牛排，搭配侍酒師推薦的自然酒",
            price=1200.0,
            nutrition_info=NutritionInfo(calories=850, protein=65.0, carbs=5.0, fat=58.0)
        )
        restaurant2.add_menu_item(menu_item2_1)
        
        restaurants.append(restaurant2)
        
        # 餐廳 3
        restaurant3 = Restaurant(
            restaurant_id="rest_003",
            name="晨光烘焙坊",
            address="台中市南屯區公益路二段51號",
            latitude=24.1400,
            longitude=120.6400,
            google_map_link="https://maps.google.com/?q=24.1400,120.6400",
            average_rating=4.3
        )
        
        menu_item3_1 = MenuItem(
            item_id="item_004",
            name="手工可頌",
            description="每日清晨現烤，手工可頌與單品咖啡的經典組合",
            price=120.0,
            nutrition_info=NutritionInfo(calories=280, protein=6.0, carbs=32.0, fat=14.0)
        )
        restaurant3.add_menu_item(menu_item3_1)
        
        restaurants.append(restaurant3)
        
        return restaurants

    @staticmethod
    def create_sample_users() -> List[User]:
        """建立範例使用者資料"""
        users = []
        
        # 使用者 1 - 一般模式
        user1 = User(
            user_id="user_001",
            username="alice",
            hashed_password="hashed_password_here"
        )
        user1.profile = UserProfile(
            budget=500.0,
            mode=AppMode.NORMAL
        )
        users.append(user1)
        
        # 使用者 2 - 健身模式
        user2 = User(
            user_id="user_002",
            username="bob",
            hashed_password="hashed_password_here"
        )
        health_goal = HealthProfile(
            target_calories=2000,
            target_protein=150.0,
            target_fat=60.0
        )
        user2.profile = UserProfile(
            budget=800.0,
            mode=AppMode.FITNESS,
            health_goal=health_goal
        )
        users.append(user2)
        
        # 使用者 3 - 觀光模式
        user3 = User(
            user_id="user_003",
            username="charlie",
            hashed_password="hashed_password_here"
        )
        user3.profile = UserProfile(
            budget=1000.0,
            mode=AppMode.TOURIST
        )
        users.append(user3)
        
        return users
