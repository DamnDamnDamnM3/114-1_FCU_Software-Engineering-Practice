USE data;

-- 建立用戶資料表
CREATE TABLE IF NOT EXISTS users (
    user_id         INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    mode            ENUM('NORMAL', 'FITNESS') DEFAULT 'NORMAL',
    budget          DECIMAL(8,2) DEFAULT 0,       -- 單餐預算上限
    target_calories INT,
    target_protein  FLOAT,
    target_fat      FLOAT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 建立餐廳資料表
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id     INT AUTO_INCREMENT PRIMARY KEY,
    name              VARCHAR(100) NOT NULL,
    address           VARCHAR(255),
    average_rating    FLOAT DEFAULT 0,
    price_range       TINYINT,           -- 1 平價, 2 中等, 3 高檔
    food_type         VARCHAR(50),       -- 日式、義式...
    vegetarian_option ENUM('VEGAN', 'LACTO_OVO', 'NON_VEG')
) ENGINE=InnoDB;

-- 建立餐點資料表
CREATE TABLE IF NOT EXISTS menu_items (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name          VARCHAR(100) NOT NULL,
    description   TEXT,
    price         DECIMAL(8,2) NOT NULL,  -- 實際比對 budget
    calories      INT,
    protein       FLOAT,
    carbs         FLOAT,
    fat           FLOAT,
    CONSTRAINT fk_menu_restaurant
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 建立飲食紀錄資料表
CREATE TABLE IF NOT EXISTS diet_logs (
    log_id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    item_id      INT NOT NULL,
    timestamp    DATETIME NOT NULL,
    portion_size FLOAT DEFAULT 1.0,
    CONSTRAINT fk_diet_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_diet_item
        FOREIGN KEY (item_id)
        REFERENCES menu_items(item_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 建立評論資料表
CREATE TABLE IF NOT EXISTS reviews (
    review_id     INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    user_id       INT NOT NULL,
    rating        INT NOT NULL,
    comment       TEXT,
    timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_restaurant
        FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 建議索引
CREATE INDEX idx_menu_restaurant    ON menu_items(restaurant_id);
CREATE INDEX idx_diet_user_time     ON diet_logs(user_id, timestamp);
CREATE INDEX idx_review_restaurant  ON reviews(restaurant_id);
