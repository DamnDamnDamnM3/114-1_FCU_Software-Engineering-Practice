"""
Restaurant 模組路由
實作餐廳搜尋、推薦、飲食記錄和分析功能
"""

from flask import jsonify, request
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from . import restaurant_bp
from services.search_service import SearchService
from services.recommendation_service import RecommendationService
from services.analytics_service import AnalyticsService
from models.filter_criteria import FilterCriteria
from models.user import User
from models.diet_log import DietLog
from models.menu_item import MenuItem
from data.sample_data import SampleData
from utils.debug import INFO_PRINT, ERROR_PRINT, WARN_PRINT

# 初始化服務
search_service = SearchService()
recommendation_service = RecommendationService()
analytics_service = AnalyticsService()

# 範例資料（實際應用中應該從資料庫讀取）
_sample_restaurants = SampleData.create_sample_restaurants()
_sample_users = SampleData.create_sample_users()


def _find_restaurant_by_id(restaurant_id: str):
    """根據 ID 尋找餐廳"""
    for restaurant in _sample_restaurants:
        if restaurant.restaurant_id == restaurant_id:
            return restaurant
    return None


def _find_menu_item_by_id(item_id: str):
    """根據 ID 尋找菜單項目"""
    for restaurant in _sample_restaurants:
        for menu_item in restaurant.menu_items:
            if menu_item.item_id == item_id:
                return menu_item
    return None


def _find_user_by_id(user_id: str):
    """根據 ID 尋找使用者（實際應用中應該從資料庫讀取）"""
    for user in _sample_users:
        if user.user_id == user_id:
            return user
    return None


@restaurant_bp.route("/", methods=["GET"])
def list_restaurants():
    """
    列出所有餐廳
    
    Returns:
        JSON: 餐廳列表
    """
    try:
        restaurants_data = []
        for restaurant in _sample_restaurants:
            restaurants_data.append({
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "address": restaurant.address,
                "average_rating": restaurant.average_rating,
                "menu_item_count": len(restaurant.menu_items),
                "review_count": len(restaurant.reviews)
            })
        
        return jsonify({
            "success": True,
            "data": restaurants_data,
            "count": len(restaurants_data)
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 列出餐廳時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得餐廳列表"
        }), 500


@restaurant_bp.route("/search", methods=["GET", "POST"])
def search_restaurants():
    """
    搜尋餐廳
    
    GET/POST 參數:
        keyword: 關鍵字
        max_price: 最高價格
        min_rating: 最低評分
        sort_by: 排序方式 (price, rating, distance)
    
    Returns:
        JSON: 符合條件的餐廳列表
    """
    try:
        # 取得搜尋條件
        if request.method == "POST":
            data = request.get_json() or {}
            keyword = data.get("keyword")
            max_price = data.get("max_price")
            min_rating = data.get("min_rating")
            sort_by = data.get("sort_by")
        else:
            keyword = request.args.get("keyword")
            max_price = request.args.get("max_price", type=float)
            min_rating = request.args.get("min_rating", type=float)
            sort_by = request.args.get("sort_by")
        
        # 建立篩選條件
        criteria = FilterCriteria(
            keyword=keyword,
            max_price=max_price,
            min_rating=min_rating,
            sort_by=sort_by
        )
        
        # 執行搜尋
        results = search_service.search_restaurants(criteria)
        
        # 轉換為 JSON 格式
        restaurants_data = []
        for restaurant in results:
            restaurants_data.append({
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "address": restaurant.address,
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
                "google_map_link": restaurant.google_map_link,
                "average_rating": restaurant.average_rating,
                "menu_item_count": len(restaurant.menu_items),
                "review_count": len(restaurant.reviews)
            })
        
        return jsonify({
            "success": True,
            "data": restaurants_data,
            "count": len(restaurants_data),
            "criteria": {
                "keyword": keyword,
                "max_price": max_price,
                "min_rating": min_rating,
                "sort_by": sort_by
            }
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 搜尋餐廳時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "搜尋失敗"
        }), 500


@restaurant_bp.route("/<restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id: str):
    """
    取得餐廳詳情
    
    Args:
        restaurant_id: 餐廳 ID
    
    Returns:
        JSON: 餐廳詳情
    """
    try:
        restaurant = _find_restaurant_by_id(restaurant_id)
        
        if not restaurant:
            return jsonify({
                "success": False,
                "error": "餐廳不存在"
            }), 404
        
        # 轉換為 JSON 格式
        restaurant_data = {
            "restaurant_id": restaurant.restaurant_id,
            "name": restaurant.name,
            "address": restaurant.address,
            "latitude": restaurant.latitude,
            "longitude": restaurant.longitude,
            "google_map_link": restaurant.google_map_link,
            "average_rating": restaurant.average_rating,
            "menu_items": [
                {
                    "item_id": item.item_id,
                    "name": item.name,
                    "description": item.description,
                    "price": item.price,
                    "nutrition_info": {
                        "calories": item.nutrition_info.calories if item.nutrition_info else None,
                        "protein": item.nutrition_info.protein if item.nutrition_info else None,
                        "carbs": item.nutrition_info.carbs if item.nutrition_info else None,
                        "fat": item.nutrition_info.fat if item.nutrition_info else None
                    } if item.nutrition_info else None
                }
                for item in restaurant.menu_items
            ],
            "reviews": [
                {
                    "review_id": review.review_id,
                    "rating": review.rating,
                    "comment": review.comment,
                    "timestamp": review.timestamp.isoformat()
                }
                for review in restaurant.reviews
            ]
        }
        
        return jsonify({
            "success": True,
            "data": restaurant_data
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得餐廳詳情時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得餐廳詳情"
        }), 500


@restaurant_bp.route("/<restaurant_id>/menu", methods=["GET"])
def get_restaurant_menu(restaurant_id: str):
    """
    取得餐廳菜單
    
    Args:
        restaurant_id: 餐廳 ID
    
    Returns:
        JSON: 菜單列表
    """
    try:
        restaurant = _find_restaurant_by_id(restaurant_id)
        
        if not restaurant:
            return jsonify({
                "success": False,
                "error": "餐廳不存在"
            }), 404
        
        menu_data = [
            {
                "item_id": item.item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "nutrition_info": {
                    "calories": item.nutrition_info.calories if item.nutrition_info else None,
                    "protein": item.nutrition_info.protein if item.nutrition_info else None,
                    "carbs": item.nutrition_info.carbs if item.nutrition_info else None,
                    "fat": item.nutrition_info.fat if item.nutrition_info else None
                } if item.nutrition_info else None
            }
            for item in restaurant.menu_items
        ]
        
        return jsonify({
            "success": True,
            "data": menu_data,
            "count": len(menu_data)
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得餐廳菜單時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得餐廳菜單"
        }), 500


@restaurant_bp.route("/<restaurant_id>/reviews", methods=["GET", "POST"])
def restaurant_reviews(restaurant_id: str):
    """
    取得或新增餐廳評論
    
    GET: 取得評論列表
    POST: 新增評論
    
    Args:
        restaurant_id: 餐廳 ID
    
    Returns:
        JSON: 評論列表或新增結果
    """
    try:
        restaurant = _find_restaurant_by_id(restaurant_id)
        
        if not restaurant:
            return jsonify({
                "success": False,
                "error": "餐廳不存在"
            }), 404
        
        if request.method == "GET":
            # 取得評論列表
            reviews_data = [
                {
                    "review_id": review.review_id,
                    "rating": review.rating,
                    "comment": review.comment,
                    "timestamp": review.timestamp.isoformat()
                }
                for review in restaurant.reviews
            ]
            
            return jsonify({
                "success": True,
                "data": reviews_data,
                "count": len(reviews_data)
            }), 200
        
        else:  # POST
            # 新增評論
            data = request.get_json() or {}
            rating = data.get("rating")
            comment = data.get("comment", "")
            
            if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
                return jsonify({
                    "success": False,
                    "error": "評分必須是 1-5 之間的整數"
                }), 400
            
            from models.review import Review
            
            review = Review(
                review_id=str(uuid.uuid4()),
                rating=rating,
                comment=comment,
                timestamp=datetime.now()
            )
            
            restaurant.add_review(review)
            
            return jsonify({
                "success": True,
                "message": "評論已新增",
                "data": {
                    "review_id": review.review_id,
                    "rating": review.rating,
                    "comment": review.comment,
                    "timestamp": review.timestamp.isoformat()
                }
            }), 201
    
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 處理餐廳評論時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "操作失敗"
        }), 500


@restaurant_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    """
    取得推薦菜單項目
    
    GET 參數:
        user_id: 使用者 ID（可選，如果沒有則使用預設使用者）
    
    Returns:
        JSON: 推薦的菜單項目列表
    """
    try:
        user_id = request.args.get("user_id")
        
        # 取得使用者（實際應用中應該從 session 或資料庫讀取）
        if user_id:
            user = _find_user_by_id(user_id)
        else:
            # 使用第一個範例使用者
            user = _sample_users[0] if _sample_users else None
        
        if not user:
            return jsonify({
                "success": False,
                "error": "使用者不存在"
            }), 404
        
        # 取得推薦
        recommendations = recommendation_service.get_recommendations(user)
        
        # 轉換為 JSON 格式
        recommendations_data = []
        for item in recommendations:
            recommendations_data.append({
                "item_id": item.item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "restaurant": {
                    "restaurant_id": item.restaurant.restaurant_id if item.restaurant else None,
                    "name": item.restaurant.name if item.restaurant else None
                } if item.restaurant else None,
                "nutrition_info": {
                    "calories": item.nutrition_info.calories if item.nutrition_info else None,
                    "protein": item.nutrition_info.protein if item.nutrition_info else None,
                    "carbs": item.nutrition_info.carbs if item.nutrition_info else None,
                    "fat": item.nutrition_info.fat if item.nutrition_info else None
                } if item.nutrition_info else None
            })
        
        return jsonify({
            "success": True,
            "data": recommendations_data,
            "count": len(recommendations_data),
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "mode": user.profile.mode.value if user.profile else None
            }
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得推薦時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法取得推薦"
        }), 500


@restaurant_bp.route("/diet-logs", methods=["GET", "POST"])
def diet_logs():
    """
    取得或新增飲食記錄
    
    GET: 取得飲食記錄列表
    POST: 新增飲食記錄
    
    GET 參數:
        user_id: 使用者 ID
    
    POST 資料:
        user_id: 使用者 ID
        item_id: 菜單項目 ID
        portion_size: 份量大小（可選，預設 "1"）
    
    Returns:
        JSON: 飲食記錄列表或新增結果
    """
    try:
        if request.method == "GET":
            # 取得飲食記錄列表
            user_id = request.args.get("user_id")
            
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID"
                }), 400
            
            user = _find_user_by_id(user_id)
            
            if not user:
                return jsonify({
                    "success": False,
                    "error": "使用者不存在"
                }), 404
            
            # 轉換為 JSON 格式
            logs_data = []
            for log in user.diet_logs:
                logs_data.append({
                    "log_id": log.log_id,
                    "timestamp": log.timestamp.isoformat(),
                    "portion_size": log.portion_size,
                    "menu_item": {
                        "item_id": log.menu_item.item_id,
                        "name": log.menu_item.name,
                        "price": log.menu_item.price,
                        "restaurant": {
                            "restaurant_id": log.menu_item.restaurant.restaurant_id if log.menu_item.restaurant else None,
                            "name": log.menu_item.restaurant.name if log.menu_item.restaurant else None
                        } if log.menu_item.restaurant else None
                    } if log.menu_item else None
                })
            
            return jsonify({
                "success": True,
                "data": logs_data,
                "count": len(logs_data)
            }), 200
        
        else:  # POST
            # 新增飲食記錄
            data = request.get_json() or {}
            user_id = data.get("user_id")
            item_id = data.get("item_id")
            portion_size = data.get("portion_size", "1")
            
            if not user_id or not item_id:
                return jsonify({
                    "success": False,
                    "error": "請提供使用者 ID 和菜單項目 ID"
                }), 400
            
            user = _find_user_by_id(user_id)
            menu_item = _find_menu_item_by_id(item_id)
            
            if not user:
                return jsonify({
                    "success": False,
                    "error": "使用者不存在"
                }), 404
            
            if not menu_item:
                return jsonify({
                    "success": False,
                    "error": "菜單項目不存在"
                }), 404
            
            # 建立飲食記錄
            log = DietLog.create_log(user, menu_item, portion_size)
            
            return jsonify({
                "success": True,
                "message": "飲食記錄已新增",
                "data": {
                    "log_id": log.log_id,
                    "timestamp": log.timestamp.isoformat(),
                    "portion_size": log.portion_size,
                    "menu_item": {
                        "item_id": menu_item.item_id,
                        "name": menu_item.name
                    }
                }
            }), 201
    
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 處理飲食記錄時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "操作失敗"
        }), 500


@restaurant_bp.route("/analytics", methods=["GET"])
def get_analytics():
    """
    取得飲食分析報告
    
    GET 參數:
        user_id: 使用者 ID
    
    Returns:
        JSON: 分析報告
    """
    try:
        user_id = request.args.get("user_id")
        
        if not user_id:
            return jsonify({
                "success": False,
                "error": "請提供使用者 ID"
            }), 400
        
        user = _find_user_by_id(user_id)
        
        if not user:
            return jsonify({
                "success": False,
                "error": "使用者不存在"
            }), 404
        
        # 生成分析報告
        analysis_text = analytics_service.generate_analysis(user)
        
        return jsonify({
            "success": True,
            "data": {
                "user_id": user.user_id,
                "username": user.username,
                "analysis": analysis_text,
                "diet_log_count": len(user.diet_logs)
            }
        }), 200
    except Exception as e:
        ERROR_PRINT(f"[ERROR] 取得分析報告時發生錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": "無法生成分析報告"
        }), 500


