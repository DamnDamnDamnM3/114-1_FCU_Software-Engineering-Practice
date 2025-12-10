USE data;

-- 插入測試用戶資料
INSERT INTO users (username, hashedPassword, mode, budget, targetCalories, targetProtein, targetFat)
VALUES
('alice',   'hash_alice',   'NORMAL', 250, 2000,  75, 60),
('bob',     'hash_bob',     'FITNESS',180, 1700, 120, 50),
('charlie', 'hash_charlie', 'NORMAL', 300, 2200,  80, 70);

-- 插入測試餐廳資料
INSERT INTO restaurants (name, address, averageRating, priceRange, foodType, vegetarianOption)
VALUES
('好吃拉麵店',     '台中市西屯區XX路123號', 4.3, 2, '日式拉麵',     'NON_VEG'),
('Green Salad House', '台中市南區OO街45號',   4.6, 2, '沙拉 / 輕食', 'VEGAN'),
('健康便當舖',     '台中市北區YY路8號',     4.1, 1, '台式便當',     'LACTO_OVO');

-- 插入測試餐點資料
INSERT INTO menu_items (restaurantID, name, description, price, calories, protein, carbs, fat)
VALUES
(1, '叉燒拉麵',   '濃厚豚骨湯頭搭配叉燒肉', 180, 650, 30, 70, 25),
(1, '蔬菜拉麵',   '清爽湯頭搭配大量蔬菜',   160, 520, 18, 65, 15),
(2, '地中海沙拉', '橄欖油與堅果的高蛋白沙拉', 190, 430, 20, 35, 18),
(2, '豆腐能量碗', '豆腐與藜麥的高蛋白組合',   210, 480, 25, 40, 16),
(3, '烤雞胸便當', '低脂雞胸搭配糙米與青菜',   120, 550, 35, 60, 12),
(3, '和風魚排便當','魚排配時蔬與白飯',       130, 600, 32, 68, 14);

-- 插入測試飲食紀錄（假設今天日期）
INSERT INTO diet_logs (userID, itemID, timestamp, portionSize)
VALUES
(1, 1, NOW() - INTERVAL 6 HOUR, 1.0),
(1, 3, NOW() - INTERVAL 1 HOUR, 0.5),
(2, 4, NOW() - INTERVAL 5 HOUR, 1.0),
(2, 5, NOW() - INTERVAL 2 HOUR, 1.0),
(3, 6, NOW() - INTERVAL 3 HOUR, 1.0);

-- 插入測試評論
INSERT INTO reviews (restaurantID, userID, rating, comment, timestamp)
VALUES
(1, 1, 5, '湯頭很讚，叉燒也很好吃！',         NOW() - INTERVAL 1 DAY),
(1, 2, 4, '份量足夠，但稍微有點鹹。',           NOW() - INTERVAL 12 HOUR),
(2, 2, 5, '對健身很友善的沙拉，蛋白質夠高。',   NOW() - INTERVAL 2 DAY),
(3, 3, 4, '便當便宜又不油，CP 值不錯。',        NOW() - INTERVAL 3 DAY);
