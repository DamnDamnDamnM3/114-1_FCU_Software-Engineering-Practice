import csv
import random

# ==========================================
# 1. 資料設定 (跟之前一樣)
# ==========================================
STORE_NAMES = {
    "台式": ["阿婆古早味", "老陳控肉飯", "逢甲大腸包小腸", "巷口乾麵", "大胃王滷肉飯", "夜市雞排", "王記熱炒", "古早味蛋餅"],
    "日式": ["ㄧ魂拉麵", "築地壽司", "大阪燒肉", "日式咖哩屋", "深夜居酒屋", "博多豚骨", "滑蛋豬排"],
    "義式": ["Luigi義大利麵", "拿坡里披薩", "米蘭燉飯", "義式小廚房", "托斯卡尼"],
    "健康餐": ["肌肉海灘餐盒", "輕食光沙拉", "低卡廚房", "水煮肌"],
    "飲品": ["50嵐(逢甲店)", "可不可熟成紅茶", "迷客夏", "路易莎咖啡", "茶湯會"],
    "韓式": ["歐巴炸雞", "韓式部隊鍋", "石鍋拌飯", "首爾泡菜鍋"]
}

MENU_TEMPLATES = {
    "台式": [
        ["招牌滷肉飯", 45, 550, 15, 60, 25], ["燙青菜", 40, 60, 2, 10, 1], ["貢丸湯", 35, 120, 8, 5, 8], ["雞排", 80, 650, 35, 40, 35]
    ],
    "日式": [
        ["豚骨拉麵", 180, 700, 25, 80, 30], ["炸豬排定食", 200, 850, 30, 90, 40], ["鮭魚丼", 250, 600, 40, 70, 20], ["味噌湯", 30, 50, 4, 6, 2]
    ],
    "義式": [
        ["白醬培根麵", 190, 750, 20, 85, 35], ["瑪格麗特披薩", 220, 800, 25, 90, 35], ["凱薩沙拉", 150, 350, 10, 20, 25]
    ],
    "健康餐": [
        ["舒肥雞胸餐盒", 130, 450, 45, 50, 8], ["香煎鮭魚飯", 160, 550, 35, 55, 15], ["無糖豆漿", 25, 100, 10, 8, 4]
    ],
    "飲品": [
        ["珍珠奶茶", 60, 500, 2, 80, 20], ["無糖綠茶", 30, 0, 0, 0, 0], ["拿鐵咖啡", 80, 180, 8, 12, 10]
    ],
    "韓式": [
        ["韓式炸雞", 220, 900, 40, 60, 50], ["泡菜豆腐鍋", 160, 600, 30, 40, 30], ["石鍋拌飯", 180, 700, 20, 90, 25]
    ]
}

ADDRESSES = ["逢甲路", "文華路", "福星路", "西安街", "河南路二段"]

# ==========================================
# 2. 生成邏輯
# ==========================================
def generate_mock_data(total_restaurants=30):
    restaurants = []
    menu_items = []
    
    types_list = list(STORE_NAMES.keys())
    item_counter = 1  # 餐點編號從1開始
    
    for i in range(total_restaurants):
        f_type = types_list[i % len(types_list)]
        base_name = random.choice(STORE_NAMES[f_type])
        r_name = f"{base_name}" if i < 15 else f"{base_name} ({i+1}號店)"
        r_id = str(i + 1)  # 餐廳編號從1開始
        
        if f_type in ["健康餐", "義式", "飲品"]:
            veg_opt = random.choice(["蛋奶素", "全素"])
        else:
            veg_opt = "葷食"
            
        # 餐廳物件
        restaurants.append({
            "restaurantID": r_id,
            "name": r_name,
            "address": f"台中市西屯區{random.choice(ADDRESSES)}{random.randint(1, 300)}號",
            "averageRating": round(random.uniform(3.5, 4.9), 1),
            "priceRange": 3 if f_type in ["日式", "義式"] else (2 if f_type in ["韓式", "健康餐"] else 1),
            "foodType": f_type,
            "vegetarianOption": veg_opt
        })
        
        # 菜單物件
        templates = MENU_TEMPLATES[f_type]
        selected_dishes = random.sample(templates, k=random.randint(2, len(templates)))
        
        for dish in selected_dishes:
            price_var = dish[1] + random.choice([-5, 0, 5, 10])
            cal_var = int(dish[2] * random.uniform(0.9, 1.1))
            
            menu_items.append({
                "itemID": str(item_counter),  # 餐點編號從1開始
                "restaurantID": r_id,
                "name": dish[0],
                "description": f"{r_name} 特製的{dish[0]}",
                "price": float(price_var),
                "calories": cal_var,
                "protein": round(dish[3] * random.uniform(0.9, 1.1), 1),
                "carbs": round(dish[4] * random.uniform(0.9, 1.1), 1),
                "fat": round(dish[5] * random.uniform(0.9, 1.1), 1)
            })
            item_counter += 1  # 遞增餐點編號

    return restaurants, menu_items

# ==========================================
# 3. 存檔 (使用內建 csv 模組，不需 pandas)
# ==========================================
def save_to_csv(filename, data, fieldnames):
    # utf-8-sig 讓 Excel 打開不會亂碼
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"成功產生: {filename} ({len(data)} 筆)")

if __name__ == "__main__":
    r_data, m_data = generate_mock_data(30)
    
    # 定義欄位順序
    r_cols = ["restaurantID", "name", "address", "averageRating", "priceRange", "foodType", "vegetarianOption"]
    m_cols = ["itemID", "restaurantID", "name", "description", "price", "calories", "protein", "carbs", "fat"]
    
    save_to_csv("restaurants.csv", r_data, r_cols)
    save_to_csv("menu_items.csv", m_data, m_cols)