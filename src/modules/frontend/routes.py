"""
Frontend 模組的路由定義
"""

from flask import render_template, jsonify, request
from . import frontend_bp
from services.restaurant_service import RestaurantService
from services.diet_service import DietService
from services.db import driver_available
from utils.debug import INFO_PRINT, ERROR_PRINT

# 初始化服務
restaurant_service = RestaurantService()
diet_service = DietService()

# 模擬收藏數據（實際應用中應該從資料庫讀取）
_user_favorites = {}  # {user_id: [restaurant_id, ...]}

# 臨時使用者 ID（實際應用中應該從登入狀態取得）
TEMP_USER_ID = 1


def _find_restaurant_by_id(restaurant_id):
    """根據 ID 尋找餐廳"""
    # 支援數字或字串 ID
    if isinstance(restaurant_id, str) and restaurant_id.isdigit():
        restaurant_id = int(restaurant_id)
    elif isinstance(restaurant_id, str) and restaurant_id.startswith('rest_'):
        restaurant_id = int(restaurant_id.split('_')[1])
    
    return restaurant_service.get_restaurant_by_id(restaurant_id)


def _convert_restaurant_to_frontend_format(restaurant, user_id: str = None):
    """將餐廳資料轉換為前端格式"""
    # 使用餐廳的 price_range 欄位來決定價格等級
    price_range_map = {
        1: ('$', '$ 1 ~ 200'),
        2: ('$$', '$ 200 ~ 400'),
        3: ('$$$', '$ 400 ~ 600'),
    }
    price_meta, price_range_text = price_range_map.get(
        getattr(restaurant, 'price_range', 1), 
        ('$', '$ 1 ~ 200')
    )
    
    # 計算評分顯示
    rating_value = restaurant.average_rating
    full_stars = int(rating_value)
    has_half = (rating_value - full_stars) >= 0.5
    stars_display = '★' * full_stars + ('☆' if has_half else '') + '☆' * (5 - full_stars - (1 if has_half else 0))
    rating_display = f"{stars_display} {rating_value:.1f}"
    
    # 檢查是否收藏
    is_favorited = False
    if user_id and user_id in _user_favorites:
        is_favorited = str(restaurant.restaurant_id) in _user_favorites[user_id]
    
    # 取得餐廳 ID
    rest_num = restaurant.restaurant_id
    
    # 使用本地圖片（基於餐廳 ID 循環使用 30 張圖片）
    img_id = (rest_num - 1) % 30 + 1
    placeholder_img = f"/static/images/stores/store_{img_id}.jpg"
    
    return {
        "id": rest_num,
        "restaurant_id": restaurant.restaurant_id,
        "name": restaurant.name,
        "rating": rating_display,
        "priceRange": price_range_text,
        "priceMeta": price_meta,
        "distance": f"{0.3 + (rest_num % 10) * 0.2:.1f} km",  # 模擬距離
        "heroImg": placeholder_img,
        "description": restaurant.name,
        "address": restaurant.address,
        "foodType": getattr(restaurant, 'food_type', ''),
        "vegetarianOption": getattr(restaurant, 'vegetarian_option', '葷食'),
        "menu": [
            {
                "item_id": item.item_id,
                "name": item.name,
                "price": f"${int(item.price)}",
                "calories": getattr(item, 'calories', 0),
                "protein": getattr(item, 'protein', 0),
                "carbs": getattr(item, 'carbs', 0),
                "fat": getattr(item, 'fat', 0)
            }
            for item in restaurant.menu_items[:4]  # 取前四個菜單項目
        ],
        "is_favorited": is_favorited
    }


@frontend_bp.route('/app')
def index():
    """前端應用主頁"""
    return render_template('index.html')


@frontend_bp.route('/api/stores', methods=['GET'])
def get_stores():
    """
    取得餐廳列表（前端格式）
    
    GET 參數:
        keyword: 搜尋關鍵字
        categories: 類別（逗號分隔）
        price: 價格等級 ($, $$, $$$)
        vegetarian: 是否素食 (true/false)
        user_id: 使用者 ID（可選）
    """
    try:
        keyword = request.args.get('keyword', '').strip()
        categories = request.args.get('categories', '').split(',') if request.args.get('categories') else []
        categories = [c.strip() for c in categories if c.strip()]
        price = request.args.get('price', '').strip()
        vegetarian = request.args.get('vegetarian', 'false').lower() == 'true'
        user_id = request.args.get('user_id')
        
        # 價格等級轉換為數字
        price_range = None
        if price:
            price_map = {'$': 1, '$$': 2, '$$$': 3}
            price_range = price_map.get(price, None)
        
        # 使用資料庫服務搜尋
        results = restaurant_service.search_restaurants(
            keyword=keyword if keyword else None,
            categories=categories if categories else None,
            price_range=price_range,
            vegetarian=vegetarian
        )
        
        # 轉換為前端格式
        stores_data = []
        for restaurant in results:
            store_data = _convert_restaurant_to_frontend_format(restaurant, user_id)
            stores_data.append(store_data)
        
        return jsonify({
            "success": True,
            "data": stores_data
        }), 200
        
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得餐廳列表時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得餐廳列表"
        }), 500


@frontend_bp.route('/api/stores/<store_id>', methods=['GET'])
def get_store_detail(store_id: str):
    """
    取得餐廳詳情（前端格式）
    
    Args:
        store_id: 餐廳 ID（數字或 restaurant_id）
    """
    try:
        user_id = request.args.get('user_id')
        
        # 嘗試找到餐廳
        restaurant = None
        if store_id.isdigit():
            # 如果是數字，嘗試轉換為 restaurant_id
            restaurant_id = f"rest_{int(store_id):03d}"
            restaurant = _find_restaurant_by_id(restaurant_id)
        else:
            restaurant = _find_restaurant_by_id(store_id)
        
        if not restaurant:
            return jsonify({
                "success": False,
                "error": "餐廳不存在"
            }), 404
        
        store_data = _convert_restaurant_to_frontend_format(restaurant, user_id)
        
        return jsonify({
            "success": True,
            "data": store_data
        }), 200
        
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得餐廳詳情時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得餐廳詳情"
        }), 500


@frontend_bp.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
def manage_favorites():
    """
    管理收藏
    
    GET: 取得收藏列表
    POST: 新增收藏
    DELETE: 移除收藏
    
    POST/DELETE 資料:
        user_id: 使用者 ID
        restaurant_id: 餐廳 ID
    """
    try:
        if request.method == 'GET':
            user_id = request.args.get('user_id')
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID"
                }), 400
            
            favorites = _user_favorites.get(user_id, [])
            
            # 取得收藏的餐廳資料
            favorite_stores = []
            for restaurant_id in favorites:
                restaurant = _find_restaurant_by_id(restaurant_id)
                if restaurant:
                    favorite_stores.append(_convert_restaurant_to_frontend_format(restaurant, user_id))
            
            return jsonify({
                "success": True,
                "data": favorite_stores
            }), 200
        
        elif request.method == 'POST':
            data = request.get_json() or {}
            user_id = data.get('user_id')
            restaurant_id = data.get('restaurant_id')
            
            if not user_id or not restaurant_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID 和餐廳 ID"
                }), 400
            
            if user_id not in _user_favorites:
                _user_favorites[user_id] = []
            
            if restaurant_id not in _user_favorites[user_id]:
                _user_favorites[user_id].append(restaurant_id)
            
            return jsonify({
                "success": True,
                "message": "已加入收藏"
            }), 200
        
        else:  # DELETE
            data = request.get_json() or {}
            user_id = data.get('user_id')
            restaurant_id = data.get('restaurant_id')
            
            if not user_id or not restaurant_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID 和餐廳 ID"
                }), 400
            
            if user_id in _user_favorites:
                _user_favorites[user_id] = [r for r in _user_favorites[user_id] if r != restaurant_id]
            
            return jsonify({
                "success": True,
                "message": "已移除收藏"
            }), 200
    
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 處理收藏時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "操作失敗"
        }), 500


@frontend_bp.route('/api/restaurants/list', methods=['GET'])
def get_restaurant_list():
    """取得餐廳列表（下拉選單用）"""
    try:
        restaurants = restaurant_service.get_restaurant_list()
        return jsonify({
            "success": True,
            "data": restaurants
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得餐廳列表失敗: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得餐廳列表"
        }), 500


@frontend_bp.route('/api/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_restaurant_menu(restaurant_id):
    """取得特定餐廳的菜單"""
    try:
        restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            return jsonify({
                "success": False,
                "error": "餐廳不存在"
            }), 404
            
        menu_items = []
        for item in restaurant.menu_items:
            menu_items.append({
                "id": item.item_id,
                "name": item.name,
                "price": item.price,
                "calories": item.calories,
                "protein": item.protein,
                "carbs": item.carbs,
                "fat": item.fat,
                "sugar": 0, # 資料庫目前沒有糖和鈉，暫時設為 0
                "sodium": 0
            })
            
        return jsonify({
            "success": True,
            "data": menu_items
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得菜單失敗: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得菜單"
        }), 500


@frontend_bp.route('/api/diet', methods=['GET', 'POST', 'DELETE'])
def manage_diet():
    """
    管理飲食記錄
    
    GET: 取得飲食記錄
    POST: 新增飲食記錄（透過菜單項目 ID）
    DELETE: 刪除飲食記錄
    
    GET 參數:
        user_id: 使用者 ID（可選，預設使用臨時 ID）
        today: 是否只取今日記錄 (true/false)
    
    POST 資料:
        user_id: 使用者 ID（可選）
        item_id: 菜單項目 ID
        portion_size: 份量倍數（可選，預設 1.0）
    
    DELETE 資料:
        user_id: 使用者 ID（可選）
        log_id: 記錄 ID
    """
    try:
        if request.method == 'GET':
            user_id = request.args.get('user_id', type=int) or TEMP_USER_ID
            date_str = request.args.get('date')
            
            if date_str:
                logs = diet_service.get_date_diet_logs(user_id, date_str)
            else:
                today_only = request.args.get('today', 'true').lower() == 'true'
                if today_only:
                    logs = diet_service.get_today_diet_logs(user_id)
                else:
                    logs = diet_service.get_user_diet_logs(user_id)
            
            # 轉換為前端格式
            logs_data = []
            for log in logs:
                # 根據時間判斷餐別
                meal_type = 'other'
                if log.timestamp:
                    hour = log.timestamp.hour
                    if 5 <= hour < 11:
                        meal_type = 'breakfast'
                    elif 11 <= hour < 17:
                        meal_type = 'lunch'
                    elif 17 <= hour < 22:
                        meal_type = 'dinner'
                
                logs_data.append({
                    "id": log.log_id,
                    "item_id": log.item_id,
                    "name": log.item_name,
                    "restaurant": log.restaurant_name,
                    "cals": int(log.calories * log.portion_size),
                    "protein": round(log.protein * log.portion_size, 1),
                    "carbs": round(log.carbs * log.portion_size, 1),
                    "fat": round(log.fat * log.portion_size, 1),
                    "portion_size": log.portion_size,
                    "timestamp": log.timestamp.isoformat() if log.timestamp else None,
                    "meal": meal_type
                })
            
            # 同時返回今日營養攝取總計
            summary = diet_service.get_today_nutrition_summary(user_id)
            
            return jsonify({
                "success": True,
                "data": logs_data,
                "summary": summary
            }), 200
        
        elif request.method == 'POST':
            data = request.get_json() or {}
            
            # 處理 user_id，確保為整數
            user_id = data.get('user_id')
            if str(user_id) == 'user_001':
                user_id = TEMP_USER_ID
            else:
                try:
                    user_id = int(user_id)
                except (ValueError, TypeError):
                    user_id = TEMP_USER_ID
            
            item_id = data.get('item_id')
            portion_size = data.get('portion_size', 1.0)
            date_str = data.get('date') # 前端傳來的日期字串
            meal_type = data.get('meal') # 前端傳來的餐別

            # 根據餐別設定時間
            timestamp = None
            if date_str:
                # 如果 date_str 已經包含時間 (T)，則取日期部分
                if 'T' in date_str:
                    date_part = date_str.split('T')[0]
                else:
                    date_part = date_str

                if meal_type == 'breakfast':
                    timestamp = f"{date_part} 08:00:00"
                elif meal_type == 'lunch':
                    timestamp = f"{date_part} 12:00:00"
                elif meal_type == 'dinner':
                    timestamp = f"{date_part} 18:00:00"
                else:
                    # other 或未指定
                    from datetime import datetime
                    now = datetime.now()
                    if now.strftime('%Y-%m-%d') == date_part:
                        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        timestamp = f"{date_part} 20:00:00"
            
            if not item_id:
                return jsonify({
                    "success": False,
                    "error": "請提供菜單項目 ID"
                }), 400
            
            # 新增飲食記錄
            log_id = diet_service.add_diet_log(
                user_id=user_id,
                item_id=item_id,
                portion_size=portion_size,
                timestamp=timestamp
            )
            
            if log_id:
                return jsonify({
                    "success": True,
                    "message": "飲食記錄已新增",
                    "data": {"log_id": log_id}
                }), 201
            else:
                return jsonify({
                    "success": False,
                    "error": "新增飲食記錄失敗"
                }), 500
        
        else:  # DELETE
            data = request.get_json() or {}
            user_id = data.get('user_id') or TEMP_USER_ID
            log_id = data.get('log_id') or data.get('id')
            
            if not log_id:
                return jsonify({
                    "success": False,
                    "error": "請提供記錄 ID"
                }), 400
            
            success = diet_service.delete_diet_log(
                log_id=int(log_id),
                user_id=int(user_id)
            )
            
            if success:
                return jsonify({
                    "success": True,
                    "message": "飲食記錄已刪除"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": "刪除失敗或記錄不存在"
                }), 400
    
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 處理飲食記錄時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "操作失敗"
        }), 500

