"""
Frontend 模組的路由定義
"""

from flask import render_template, jsonify, request
from . import frontend_bp
from services.search_service import SearchService
from models.filter_criteria import FilterCriteria
from data.sample_data import SampleData
from utils.debug import INFO_PRINT, ERROR_PRINT

# 初始化服務
search_service = SearchService()

# 範例資料
_sample_restaurants = SampleData.create_sample_restaurants()

# 模擬收藏數據（實際應用中應該從資料庫讀取）
_user_favorites = {}  # {user_id: [restaurant_id, ...]}

# 模擬飲食記錄數據（實際應用中應該從資料庫讀取）
_user_diet_logs = {}  # {user_id: [{meal, name, cals, carbs, protein, fat, sugar, sodium, date}, ...]}


def _find_restaurant_by_id(restaurant_id: str):
    """根據 ID 尋找餐廳"""
    for restaurant in _sample_restaurants:
        if restaurant.restaurant_id == restaurant_id:
            return restaurant
    return None


def _convert_restaurant_to_frontend_format(restaurant, user_id: str = None):
    """將餐廳資料轉換為前端格式"""
    # 計算價格範圍
    if restaurant.menu_items:
        prices = [item.price for item in restaurant.menu_items]
        min_price = min(prices)
        max_price = max(prices)
        
        # 判斷價格等級
        if max_price <= 200:
            price_meta = '$'
            price_range = '$ 1 ~ 200'
        elif max_price <= 400:
            price_meta = '$$'
            price_range = '$ 200 ~ 400'
        elif max_price <= 600:
            price_meta = '$$$'
            price_range = '$ 400 ~ 600'
        else:
            price_meta = '$$$$'
            price_range = '$ 600+'
    else:
        price_meta = '$'
        price_range = '$ 1 ~ 200'
    
    # 計算評分顯示
    rating_value = restaurant.average_rating
    full_stars = int(rating_value)
    has_half = (rating_value - full_stars) >= 0.5
    stars_display = '★' * full_stars + ('☆' if has_half else '') + '☆' * (5 - full_stars - (1 if has_half else 0))
    rating_display = f"{stars_display} {rating_value:.1f}"
    
    # 檢查是否收藏
    is_favorited = False
    if user_id and user_id in _user_favorites:
        is_favorited = restaurant.restaurant_id in _user_favorites[user_id]
    
    return {
        "id": int(restaurant.restaurant_id.split('_')[1]) if '_' in restaurant.restaurant_id else 1,
        "restaurant_id": restaurant.restaurant_id,
        "name": restaurant.name,
        "rating": rating_display,
        "priceRange": price_range,
        "priceMeta": price_meta,
        "distance": "0.8 km",  # 模擬距離
        "heroImg": f"placeholder-store-{int(restaurant.restaurant_id.split('_')[1]) % 4 + 1}.jpg" if '_' in restaurant.restaurant_id else "placeholder-store-1.jpg",
        "description": restaurant.name,
        "address": restaurant.address,
        "menu": [
            {
                "name": item.name,
                "price": f"${int(item.price)}"
            }
            for item in restaurant.menu_items[:2]  # 只取前兩個
        ],
        "is_favorited": is_favorited
    }


@frontend_bp.route('/app')
def index():
    """前端應用主頁"""
    return render_template('frontend/index.html')


@frontend_bp.route('/api/stores', methods=['GET'])
def get_stores():
    """
    取得餐廳列表（前端格式）
    
    GET 參數:
        keyword: 搜尋關鍵字
        categories: 類別（逗號分隔）
        price: 價格等級 ($, $$, $$$, $$$$)
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
        
        # 建立篩選條件
        max_price = None
        if price:
            price_map = {'$': 200, '$$': 400, '$$$': 600, '$$$$': float('inf')}
            max_price = price_map.get(price, None)
        
        criteria = FilterCriteria(
            keyword=keyword if keyword else None,
            max_price=max_price,
            sort_by='rating'
        )
        
        # 執行搜尋
        results = search_service.search_restaurants(criteria)
        
        # 轉換為前端格式
        stores_data = []
        for restaurant in results:
            store_data = _convert_restaurant_to_frontend_format(restaurant, user_id)
            
            # 類別篩選（這裡簡化處理，實際應該從餐廳資料中取得）
            # 素食篩選（這裡簡化處理）
            if vegetarian:
                # 實際應用中應該檢查餐廳是否有素食選項
                pass
            
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


@frontend_bp.route('/api/diet', methods=['GET', 'POST', 'DELETE'])
def manage_diet():
    """
    管理飲食記錄
    
    GET: 取得飲食記錄
    POST: 新增飲食記錄
    DELETE: 刪除飲食記錄
    
    GET 參數:
        user_id: 使用者 ID
        date: 日期 (YYYY-MM-DD)
        meal: 餐次 (breakfast, lunch, dinner, other)
    
    POST 資料:
        user_id: 使用者 ID
        meal: 餐次
        name: 食物名稱
        cals: 熱量
        carbs: 碳水化合物
        protein: 蛋白質
        fat: 脂肪
        sugar: 糖
        sodium: 鈉
        date: 日期 (YYYY-MM-DD，可選，預設今天)
    """
    try:
        if request.method == 'GET':
            user_id = request.args.get('user_id')
            date = request.args.get('date')
            meal = request.args.get('meal')
            
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID"
                }), 400
            
            user_logs = _user_diet_logs.get(user_id, [])
            
            # 篩選
            filtered_logs = user_logs
            if date:
                filtered_logs = [log for log in filtered_logs if log.get('date') == date]
            if meal:
                filtered_logs = [log for log in filtered_logs if log.get('meal') == meal]
            
            return jsonify({
                "success": True,
                "data": filtered_logs
            }), 200
        
        elif request.method == 'POST':
            data = request.get_json() or {}
            user_id = data.get('user_id')
            meal = data.get('meal')
            name = data.get('name')
            cals = data.get('cals', 0)
            carbs = data.get('carbs', 0)
            protein = data.get('protein', 0)
            fat = data.get('fat', 0)
            sugar = data.get('sugar', 0)
            sodium = data.get('sodium', 0)
            date = data.get('date')
            
            if not user_id or not meal or not name:
                return jsonify({
                    "success": False,
                    "error": "請提供必要資訊"
                }), 400
            
            if user_id not in _user_diet_logs:
                _user_diet_logs[user_id] = []
            
            from datetime import datetime
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            
            new_log = {
                "id": len(_user_diet_logs[user_id]) + 1,
                "meal": meal,
                "name": name,
                "cals": int(cals),
                "carbs": float(carbs),
                "protein": float(protein),
                "fat": float(fat),
                "sugar": float(sugar),
                "sodium": float(sodium),
                "date": date
            }
            
            _user_diet_logs[user_id].append(new_log)
            
            return jsonify({
                "success": True,
                "message": "飲食記錄已新增",
                "data": new_log
            }), 201
        
        else:  # DELETE
            data = request.get_json() or {}
            user_id = data.get('user_id')
            log_id = data.get('id')
            
            if not user_id or not log_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID 和記錄 ID"
                }), 400
            
            if user_id in _user_diet_logs:
                _user_diet_logs[user_id] = [log for log in _user_diet_logs[user_id] if log.get('id') != log_id]
            
            return jsonify({
                "success": True,
                "message": "飲食記錄已刪除"
            }), 200
    
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 處理飲食記錄時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "操作失敗"
        }), 500

