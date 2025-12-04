# 資料模型與服務層實作文件

本文檔記錄了根據 UML 類別圖實作的完整資料模型與服務層架構。

## 目錄結構

```
src/
├── models/              # 資料模型
│   ├── __init__.py
│   ├── user.py          # User 類別
│   ├── user_profile.py  # UserProfile 類別
│   ├── app_mode.py      # AppMode 列舉
│   ├── health_profile.py # HealthProfile 類別
│   ├── diet_log.py      # DietLog 類別
│   ├── menu_item.py     # MenuItem 類別
│   ├── nutrition_info.py # NutritionInfo 類別
│   ├── restaurant.py    # Restaurant 類別
│   ├── review.py        # Review 類別
│   └── filter_criteria.py # FilterCriteria 類別
├── services/            # 服務層
│   ├── __init__.py
│   ├── search_service.py        # SearchService
│   ├── recommendation_service.py # RecommendationService
│   └── analytics_service.py     # AnalyticsService
└── data/                # 範例資料
    ├── __init__.py
    └── sample_data.py   # SampleData
```

## 資料模型（Models）

### User
- **欄位**: `user_id`, `username`, `hashed_password`, `profile`, `diet_logs`
- **方法**: `login()`, `register()`, `get_profile()`
- **關聯**: 
  - 1:1 與 UserProfile
  - 1:0..* 與 DietLog

### UserProfile
- **欄位**: `budget`, `mode`, `health_goal`
- **方法**: `set_budget()`, `set_mode()`, `set_health_goal()`
- **關聯**: 
  - 使用 HealthProfile (0..1)
  - 使用 AppMode (1)

### AppMode (Enum)
- **值**: `NORMAL`, `FITNESS`, `TOURIST`

### HealthProfile
- **欄位**: `target_calories`, `target_protein`, `target_fat`
- **用途**: 當 AppMode = FITNESS 時使用

### DietLog
- **欄位**: `log_id`, `timestamp`, `portion_size`, `user`, `menu_item`
- **方法**: `create_log(user, menu_item, portion_size)`
- **關聯**: 
  - 記錄一個 MenuItem (1:1)
  - 屬於一個 User (1)

### MenuItem
- **欄位**: `item_id`, `name`, `description`, `price`, `nutrition_info`, `restaurant`
- **方法**: `get_nutrition_info()`
- **關聯**: 
  - 有 0..1 NutritionInfo
  - 屬於多個 Restaurant

### NutritionInfo
- **欄位**: `calories`, `protein`, `carbs`, `fat`

### Restaurant
- **欄位**: `restaurant_id`, `name`, `address`, `latitude`, `longitude`, `google_map_link`, `average_rating`, `menu_items`, `reviews`
- **方法**: `get_menu()`, `get_reviews()`, `add_menu_item()`, `add_review()`, `_update_average_rating()`
- **關聯**: 
  - 有多個 MenuItem (1:0..*)
  - 有多個 Review (0..*)

### Review
- **欄位**: `review_id`, `rating`, `comment`, `timestamp`, `restaurant`

### FilterCriteria
- **欄位**: `keyword`, `max_price`, `min_rating`, `sort_by`
- **用途**: 用於搜尋服務

## 服務層（Services）

### SearchService
- **方法**: `search_restaurants(criteria: FilterCriteria) -> List[Restaurant]`
- **功能**: 處理關鍵字搜尋、價格篩選、評分排序等邏輯
- **狀態**: 方法框架已建立，演算法以 TODO 標記

### RecommendationService
- **方法**: `get_recommendations(user: User) -> List[MenuItem]`
- **功能**: 使用 UserProfile、HealthProfile、DietLog、NutritionInfo 生成推薦
- **狀態**: 方法框架已建立，演算法以 TODO 標記，包含完整的資料收集流程說明

### AnalyticsService
- **方法**: `generate_analysis(user: User) -> str`
- **功能**: 對 DietLogs 與 NutritionInfo 做統計分析
- **狀態**: 方法框架已建立，分析策略以 TODO 標記

## 範例資料（SampleData）

### 功能
- `create_sample_restaurants()`: 建立範例餐廳資料（包含菜單和評論）
- `create_sample_users()`: 建立範例使用者資料（包含不同模式的使用者）

## 實作狀態

### ✅ 已完成
1. 所有資料模型類別已建立
2. 所有欄位和方法簽名已實作
3. 類別之間的關聯已建立
4. 服務層框架已建立
5. 範例資料生成器已建立
6. 循環引用問題已解決
7. 所有模組可正常導入

### 🔄 待實作（以 TODO 標記）
1. **SearchService.search_restaurants()**: 搜尋演算法
2. **RecommendationService.get_recommendations()**: 推薦演算法
3. **AnalyticsService.generate_analysis()**: 分析演算法
4. **User.login()**: 登入驗證邏輯
5. **User.register()**: 註冊邏輯

## 使用範例

```python
from src.models import User, UserProfile, AppMode, Restaurant, MenuItem
from src.services import SearchService, RecommendationService, AnalyticsService
from src.data import SampleData

# 建立範例資料
restaurants = SampleData.create_sample_restaurants()
users = SampleData.create_sample_users()

# 使用服務
search_service = SearchService()
recommendation_service = RecommendationService()
analytics_service = AnalyticsService()

# 搜尋餐廳（演算法待實作）
from src.models import FilterCriteria
criteria = FilterCriteria(keyword="牛排", max_price=1500.0, min_rating=4.0)
results = search_service.search_restaurants(criteria)

# 取得推薦（演算法待實作）
user = users[0]
recommendations = recommendation_service.get_recommendations(user)

# 生成分析報告（演算法待實作）
analysis = analytics_service.generate_analysis(user)
```

## 注意事項

1. **演算法預留**: 所有核心演算法（搜尋、推薦、分析）都以 TODO 標記，保留實作空間
2. **資料流程**: 基本資料流程已建立（例如 Restaurant 內部用 list 存 menu items）
3. **可擴充性**: 方法簽名完整，可隨時加入具體實作
4. **循環引用**: 已使用 TYPE_CHECKING 和字串註解解決循環引用問題


