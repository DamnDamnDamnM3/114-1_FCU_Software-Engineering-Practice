"""
資料載入器 - 從 dataset CSV 檔案載入餐廳和菜單資料
"""

import csv
import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class MenuItem:
    """菜單項目"""
    name: str
    price: float
    description: str = ""
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0


@dataclass
class Restaurant:
    """餐廳資料"""
    restaurant_id: str
    name: str
    address: str
    average_rating: float
    menu_items: List[MenuItem] = field(default_factory=list)
    food_type: str = ""
    price_range: int = 1  # 1=$, 2=$$, 3=$$$
    vegetarian_option: str = "葷食"  # 葷食, 蛋奶素, 全素


class SampleData:
    """從 CSV 載入餐廳資料"""
    
    _cached_restaurants: Optional[List[Restaurant]] = None
    
    @staticmethod
    def _get_dataset_path() -> str:
        """取得 dataset 資料夾路徑"""
        # 從 src/data/ 往上找到專案根目錄的 dataset/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        project_root = os.path.dirname(src_dir)
        return os.path.join(project_root, "dataset")
    
    @staticmethod
    def create_sample_restaurants() -> List[Restaurant]:
        """從 CSV 載入餐廳資料"""
        # 使用快取避免重複讀取
        if SampleData._cached_restaurants is not None:
            return SampleData._cached_restaurants
        
        dataset_path = SampleData._get_dataset_path()
        restaurants_file = os.path.join(dataset_path, "restaurants.csv")
        menu_items_file = os.path.join(dataset_path, "menu_items.csv")
        
        restaurants: List[Restaurant] = []
        menu_by_restaurant: dict = {}  # {restaurant_id: [MenuItem, ...]}
        
        # 1. 先載入菜單資料
        try:
            with open(menu_items_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rest_id = row['restaurantID']
                    menu_item = MenuItem(
                        name=row['name'],
                        price=float(row['price']),
                        description=row.get('description', ''),
                        calories=float(row.get('calories', 0)),
                        protein=float(row.get('protein', 0)),
                        carbs=float(row.get('carbs', 0)),
                        fat=float(row.get('fat', 0))
                    )
                    if rest_id not in menu_by_restaurant:
                        menu_by_restaurant[rest_id] = []
                    menu_by_restaurant[rest_id].append(menu_item)
        except FileNotFoundError:
            print(f"[WARN] 找不到菜單檔案: {menu_items_file}")
        except Exception as e:
            print(f"[ERROR] 載入菜單時發生錯誤: {e}")
        
        # 2. 載入餐廳資料
        try:
            with open(restaurants_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader, start=1):
                    rest_id = str(idx)  # CSV 沒有 ID，用行號當 ID
                    
                    restaurant = Restaurant(
                        restaurant_id=f"rest_{idx:03d}",
                        name=row['name'],
                        address=row['address'],
                        average_rating=float(row['averageRating']),
                        food_type=row.get('foodType', ''),
                        price_range=int(row.get('priceRange', 1)),
                        vegetarian_option=row.get('vegetarianOption', '葷食'),
                        menu_items=menu_by_restaurant.get(rest_id, [])
                    )
                    restaurants.append(restaurant)
        except FileNotFoundError:
            print(f"[WARN] 找不到餐廳檔案: {restaurants_file}，使用預設資料")
            restaurants = SampleData._create_fallback_data()
        except Exception as e:
            print(f"[ERROR] 載入餐廳時發生錯誤: {e}")
            restaurants = SampleData._create_fallback_data()
        
        SampleData._cached_restaurants = restaurants
        return restaurants
    
    @staticmethod
    def _create_fallback_data() -> List[Restaurant]:
        """當 CSV 無法載入時的備用資料"""
        return [
            Restaurant(
                restaurant_id="rest_001",
                name="範例餐廳",
                address="台中市西屯區逢甲路1號",
                average_rating=4.0,
                food_type="台式",
                price_range=1,
                vegetarian_option="葷食",
                menu_items=[MenuItem("招牌套餐", 100.0, "美味套餐")]
            )
        ]
    
    @staticmethod
    def clear_cache():
        """清除快取（開發/測試用）"""
        SampleData._cached_restaurants = None

