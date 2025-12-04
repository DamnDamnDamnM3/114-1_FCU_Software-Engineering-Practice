# Restaurant API 文件

本文檔說明餐廳搜尋、推薦、飲食記錄和分析功能的 API 端點。

## 基礎 URL

所有 API 端點的前綴為 `/restaurants`

## API 端點

### 1. 列出所有餐廳

**GET** `/restaurants/`

取得所有餐廳的基本資訊列表。

**回應範例：**
```json
{
  "success": true,
  "data": [
    {
      "restaurant_id": "rest_001",
      "name": "海鹽慢食",
      "address": "台中市西屯區台灣大道三段99號",
      "average_rating": 4.5,
      "menu_item_count": 2,
      "review_count": 2
    }
  ],
  "count": 3
}
```

---

### 2. 搜尋餐廳

**GET** `/restaurants/search`  
**POST** `/restaurants/search`

根據條件搜尋餐廳。

**GET 參數：**
- `keyword` (string, 可選): 關鍵字
- `max_price` (float, 可選): 最高價格
- `min_rating` (float, 可選): 最低評分
- `sort_by` (string, 可選): 排序方式 (price, rating, distance)

**POST 資料：**
```json
{
  "keyword": "牛排",
  "max_price": 1500.0,
  "min_rating": 4.0,
  "sort_by": "rating"
}
```

**回應範例：**
```json
{
  "success": true,
  "data": [...],
  "count": 2,
  "criteria": {
    "keyword": "牛排",
    "max_price": 1500.0,
    "min_rating": 4.0,
    "sort_by": "rating"
  }
}
```

---

### 3. 取得餐廳詳情

**GET** `/restaurants/<restaurant_id>`

取得指定餐廳的完整資訊，包含菜單和評論。

**回應範例：**
```json
{
  "success": true,
  "data": {
    "restaurant_id": "rest_001",
    "name": "海鹽慢食",
    "address": "台中市西屯區台灣大道三段99號",
    "latitude": 24.1794,
    "longitude": 120.6444,
    "google_map_link": "https://maps.google.com/?q=24.1794,120.6444",
    "average_rating": 4.5,
    "menu_items": [
      {
        "item_id": "item_001",
        "name": "地中海沙拉",
        "description": "結合地中海香氣與在地蔬果",
        "price": 280.0,
        "nutrition_info": {
          "calories": 350,
          "protein": 12.0,
          "carbs": 25.0,
          "fat": 18.0
        }
      }
    ],
    "reviews": [
      {
        "review_id": "rev_001",
        "rating": 5,
        "comment": "非常健康的選擇，食材新鮮",
        "timestamp": "2024-12-02T10:00:00"
      }
    ]
  }
}
```

---

### 4. 取得餐廳菜單

**GET** `/restaurants/<restaurant_id>/menu`

取得指定餐廳的菜單列表。

**回應範例：**
```json
{
  "success": true,
  "data": [
    {
      "item_id": "item_001",
      "name": "地中海沙拉",
      "description": "結合地中海香氣與在地蔬果",
      "price": 280.0,
      "nutrition_info": {
        "calories": 350,
        "protein": 12.0,
        "carbs": 25.0,
        "fat": 18.0
      }
    }
  ],
  "count": 2
}
```

---

### 5. 取得或新增餐廳評論

**GET** `/restaurants/<restaurant_id>/reviews`  
**POST** `/restaurants/<restaurant_id>/reviews`

**GET**: 取得餐廳的評論列表

**POST**: 新增評論

**POST 資料：**
```json
{
  "rating": 5,
  "comment": "非常推薦！"
}
```

**回應範例（POST）：**
```json
{
  "success": true,
  "message": "評論已新增",
  "data": {
    "review_id": "uuid-here",
    "rating": 5,
    "comment": "非常推薦！",
    "timestamp": "2024-12-02T10:00:00"
  }
}
```

---

### 6. 取得推薦

**GET** `/restaurants/recommendations`

根據使用者資料取得推薦的菜單項目。

**參數：**
- `user_id` (string, 可選): 使用者 ID，如果沒有提供則使用預設使用者

**回應範例：**
```json
{
  "success": true,
  "data": [
    {
      "item_id": "item_001",
      "name": "地中海沙拉",
      "description": "結合地中海香氣與在地蔬果",
      "price": 280.0,
      "restaurant": {
        "restaurant_id": "rest_001",
        "name": "海鹽慢食"
      },
      "nutrition_info": {
        "calories": 350,
        "protein": 12.0,
        "carbs": 25.0,
        "fat": 18.0
      }
    }
  ],
  "count": 3,
  "user": {
    "user_id": "user_001",
    "username": "alice",
    "mode": "NORMAL"
  }
}
```

---

### 7. 取得或新增飲食記錄

**GET** `/restaurants/diet-logs`  
**POST** `/restaurants/diet-logs`

**GET**: 取得使用者的飲食記錄列表

**參數：**
- `user_id` (string, 必需): 使用者 ID

**POST**: 新增飲食記錄

**POST 資料：**
```json
{
  "user_id": "user_001",
  "item_id": "item_001",
  "portion_size": "1"
}
```

**回應範例（GET）：**
```json
{
  "success": true,
  "data": [
    {
      "log_id": "log_001",
      "timestamp": "2024-12-02T10:00:00",
      "portion_size": "1",
      "menu_item": {
        "item_id": "item_001",
        "name": "地中海沙拉",
        "price": 280.0,
        "restaurant": {
          "restaurant_id": "rest_001",
          "name": "海鹽慢食"
        }
      }
    }
  ],
  "count": 5
}
```

---

### 8. 取得分析報告

**GET** `/restaurants/analytics`

取得使用者的飲食分析報告。

**參數：**
- `user_id` (string, 必需): 使用者 ID

**回應範例：**
```json
{
  "success": true,
  "data": {
    "user_id": "user_001",
    "username": "alice",
    "analysis": "分析報告（待實作）",
    "diet_log_count": 5
  }
}
```

## 錯誤回應

所有錯誤回應都遵循以下格式：

```json
{
  "success": false,
  "error": "錯誤訊息"
}
```

常見的 HTTP 狀態碼：
- `200`: 成功
- `201`: 建立成功
- `400`: 請求參數錯誤
- `404`: 資源不存在
- `500`: 伺服器錯誤

## 使用範例

### 使用 curl

```bash
# 列出所有餐廳
curl http://localhost:5000/restaurants/

# 搜尋餐廳
curl "http://localhost:5000/restaurants/search?keyword=牛排&min_rating=4.0"

# 取得餐廳詳情
curl http://localhost:5000/restaurants/rest_001

# 取得推薦
curl "http://localhost:5000/restaurants/recommendations?user_id=user_001"

# 新增飲食記錄
curl -X POST http://localhost:5000/restaurants/diet-logs \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "item_id": "item_001", "portion_size": "1"}'
```

### 使用 Python requests

```python
import requests

BASE_URL = "http://localhost:5000/restaurants"

# 列出所有餐廳
response = requests.get(f"{BASE_URL}/")
print(response.json())

# 搜尋餐廳
response = requests.get(f"{BASE_URL}/search", params={
    "keyword": "牛排",
    "min_rating": 4.0
})
print(response.json())

# 新增飲食記錄
response = requests.post(f"{BASE_URL}/diet-logs", json={
    "user_id": "user_001",
    "item_id": "item_001",
    "portion_size": "1"
})
print(response.json())
```

