"""
餐廳資料庫服務
從資料庫讀取餐廳和菜單資料
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from services.db import fetch_all, fetch_one, driver_available, DatabaseError


@dataclass
class MenuItem:
    """菜單項目"""
    item_id: int
    restaurant_id: int
    name: str
    price: float
    description: str = ""
    calories: int = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0


@dataclass
class Restaurant:
    """餐廳資料"""
    restaurant_id: int
    name: str
    address: str
    average_rating: float
    price_range: int = 1
    food_type: str = ""
    vegetarian_option: str = "葷食"
    menu_items: List[MenuItem] = field(default_factory=list)


class RestaurantService:
    """餐廳資料庫服務"""
    
    @staticmethod
    def get_restaurant_list() -> List[Dict[str, Any]]:
        """取得餐廳列表（僅 ID 和名稱）"""
        if not driver_available():
            return []
        
        try:
            query = "SELECT restaurantID, name FROM restaurants ORDER BY name"
            rows = fetch_all(query)
            return [{'id': row['restaurantID'], 'name': row['name']} for row in rows]
        except DatabaseError as e:
            print(f"[ERROR] 讀取餐廳列表失敗: {e}")
            return []

    @staticmethod
    def get_all_restaurants() -> List[Restaurant]:
        """取得所有餐廳（含菜單）"""
        if not driver_available():
            return []
        
        try:
            # 查詢所有餐廳
            query = """
                SELECT restaurantID, name, address, averageRating, 
                       priceRange, foodType, vegetarianOption
                FROM restaurants
                ORDER BY averageRating DESC
            """
            rows = fetch_all(query)
            
            restaurants = []
            for row in rows:
                restaurant = Restaurant(
                    restaurant_id=row['restaurantID'],
                    name=row['name'],
                    address=row['address'] or '',
                    average_rating=float(row['averageRating'] or 0),
                    price_range=int(row['priceRange'] or 1),
                    food_type=row['foodType'] or '',
                    vegetarian_option=row['vegetarianOption'] or '葷食',
                    menu_items=[]
                )
                
                # 查詢該餐廳的菜單
                menu_query = """
                    SELECT itemID, restaurantID, name, description, price,
                           calories, protein, carbs, fat
                    FROM menu_items
                    WHERE restaurantID = ?
                """
                menu_rows = fetch_all(menu_query, (restaurant.restaurant_id,))
                
                for menu_row in menu_rows:
                    menu_item = MenuItem(
                        item_id=menu_row['itemID'],
                        restaurant_id=menu_row['restaurantID'],
                        name=menu_row['name'],
                        price=float(menu_row['price'] or 0),
                        description=menu_row['description'] or '',
                        calories=int(menu_row['calories'] or 0),
                        protein=float(menu_row['protein'] or 0),
                        carbs=float(menu_row['carbs'] or 0),
                        fat=float(menu_row['fat'] or 0)
                    )
                    restaurant.menu_items.append(menu_item)
                
                restaurants.append(restaurant)
            
            return restaurants
            
        except DatabaseError as e:
            print(f"[ERROR] 讀取餐廳資料失敗: {e}")
            return []
    
    @staticmethod
    def get_restaurant_by_id(restaurant_id: int) -> Optional[Restaurant]:
        """根據 ID 取得單一餐廳"""
        if not driver_available():
            return None
        
        try:
            query = """
                SELECT restaurantID, name, address, averageRating,
                       priceRange, foodType, vegetarianOption
                FROM restaurants
                WHERE restaurantID = ?
            """
            row = fetch_one(query, (restaurant_id,))
            
            if not row:
                return None
            
            restaurant = Restaurant(
                restaurant_id=row['restaurantID'],
                name=row['name'],
                address=row['address'] or '',
                average_rating=float(row['averageRating'] or 0),
                price_range=int(row['priceRange'] or 1),
                food_type=row['foodType'] or '',
                vegetarian_option=row['vegetarianOption'] or '葷食',
                menu_items=[]
            )
            
            # 查詢菜單
            menu_query = """
                SELECT itemID, restaurantID, name, description, price,
                       calories, protein, carbs, fat
                FROM menu_items
                WHERE restaurantID = ?
            """
            menu_rows = fetch_all(menu_query, (restaurant_id,))
            
            for menu_row in menu_rows:
                menu_item = MenuItem(
                    item_id=menu_row['itemID'],
                    restaurant_id=menu_row['restaurantID'],
                    name=menu_row['name'],
                    price=float(menu_row['price'] or 0),
                    description=menu_row['description'] or '',
                    calories=int(menu_row['calories'] or 0),
                    protein=float(menu_row['protein'] or 0),
                    carbs=float(menu_row['carbs'] or 0),
                    fat=float(menu_row['fat'] or 0)
                )
                restaurant.menu_items.append(menu_item)
            
            return restaurant
            
        except DatabaseError as e:
            print(f"[ERROR] 讀取餐廳資料失敗: {e}")
            return None
    
    @staticmethod
    def search_restaurants(
        keyword: Optional[str] = None,
        categories: Optional[List[str]] = None,
        price_range: Optional[int] = None,
        vegetarian: bool = False
    ) -> List[Restaurant]:
        """搜尋餐廳"""
        if not driver_available():
            return []
        
        try:
            # 建立動態查詢
            conditions = []
            params = []
            
            base_query = """
                SELECT DISTINCT r.restaurantID, r.name, r.address, r.averageRating,
                       r.priceRange, r.foodType, r.vegetarianOption
                FROM restaurants r
                LEFT JOIN menu_items m ON r.restaurantID = m.restaurantID
                WHERE 1=1
            """
            
            # 關鍵字搜尋（餐廳名稱或菜單名稱）
            if keyword:
                conditions.append("(r.name LIKE ? OR m.name LIKE ?)")
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            
            # 類別篩選
            if categories and len(categories) > 0:
                placeholders = ','.join(['?' for _ in categories])
                conditions.append(f"r.foodType IN ({placeholders})")
                params.extend(categories)
            
            # 價格範圍篩選（精確匹配）
            if price_range is not None:
                conditions.append("r.priceRange = ?")
                params.append(price_range)
            
            # 素食篩選
            if vegetarian:
                conditions.append("r.vegetarianOption IN ('全素', '蛋奶素')")
            
            # 組合查詢
            if conditions:
                base_query += " AND " + " AND ".join(conditions)
            
            base_query += " ORDER BY r.averageRating DESC"
            
            rows = fetch_all(base_query, tuple(params))
            
            # 組裝結果
            restaurants = []
            for row in rows:
                restaurant = Restaurant(
                    restaurant_id=row['restaurantID'],
                    name=row['name'],
                    address=row['address'] or '',
                    average_rating=float(row['averageRating'] or 0),
                    price_range=int(row['priceRange'] or 1),
                    food_type=row['foodType'] or '',
                    vegetarian_option=row['vegetarianOption'] or '葷食',
                    menu_items=[]
                )
                
                # 查詢菜單
                menu_query = """
                    SELECT itemID, restaurantID, name, description, price,
                           calories, protein, carbs, fat
                    FROM menu_items
                    WHERE restaurantID = ?
                """
                menu_rows = fetch_all(menu_query, (restaurant.restaurant_id,))
                
                for menu_row in menu_rows:
                    menu_item = MenuItem(
                        item_id=menu_row['itemID'],
                        restaurant_id=menu_row['restaurantID'],
                        name=menu_row['name'],
                        price=float(menu_row['price'] or 0),
                        description=menu_row['description'] or '',
                        calories=int(menu_row['calories'] or 0),
                        protein=float(menu_row['protein'] or 0),
                        carbs=float(menu_row['carbs'] or 0),
                        fat=float(menu_row['fat'] or 0)
                    )
                    restaurant.menu_items.append(menu_item)
                
                restaurants.append(restaurant)
            
            return restaurants
            
        except DatabaseError as e:
            print(f"[ERROR] 搜尋餐廳失敗: {e}")
            return []
    
    @staticmethod
    def get_menu_item_by_id(item_id: int) -> Optional[MenuItem]:
        """根據 ID 取得單一菜單項目"""
        if not driver_available():
            return None
        
        try:
            query = """
                SELECT itemID, restaurantID, name, description, price,
                       calories, protein, carbs, fat
                FROM menu_items
                WHERE itemID = ?
            """
            row = fetch_one(query, (item_id,))
            
            if not row:
                return None
            
            return MenuItem(
                item_id=row['itemID'],
                restaurant_id=row['restaurantID'],
                name=row['name'],
                price=float(row['price'] or 0),
                description=row['description'] or '',
                calories=int(row['calories'] or 0),
                protein=float(row['protein'] or 0),
                carbs=float(row['carbs'] or 0),
                fat=float(row['fat'] or 0)
            )
            
        except DatabaseError as e:
            print(f"[ERROR] 讀取菜單項目失敗: {e}")
            return None
