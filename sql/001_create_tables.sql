USE data;

-- 建立用戶資料表
CREATE TABLE IF NOT EXISTS users (
    userID          INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    hashedPassword  VARCHAR(255) NOT NULL,
    mode            ENUM('NORMAL', 'FITNESS') DEFAULT 'NORMAL',
    budget          DECIMAL(8,2) DEFAULT 0,       -- 單餐預算上限
    targetCalories  INT,
    targetProtein   FLOAT,
    targetFat       FLOAT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 建立餐廳資料表
CREATE TABLE IF NOT EXISTS restaurants (
    restaurantID     INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(100) NOT NULL,
    address          VARCHAR(255),
    averageRating    FLOAT DEFAULT 0,
    priceRange       TINYINT,           -- 1 平價, 2 中等, 3 高檔
    foodType         VARCHAR(50),       -- 日式、義式...
    vegetarianOption ENUM('VEGAN', 'LACTO_OVO', 'NON_VEG')
) ENGINE=InnoDB;

-- 建立餐點資料表
CREATE TABLE IF NOT EXISTS menu_items (
    itemID        INT AUTO_INCREMENT PRIMARY KEY,
    restaurantID  INT NOT NULL,
    name          VARCHAR(100) NOT NULL,
    description   TEXT,
    price         DECIMAL(8,2) NOT NULL,  -- 實際比對 budget
    calories      INT,
    protein       FLOAT,
    carbs         FLOAT,
    fat           FLOAT,
    CONSTRAINT fk_menu_restaurant
        FOREIGN KEY (restaurantID)
        REFERENCES restaurants(restaurantID)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 建立飲食紀錄資料表
CREATE TABLE IF NOT EXISTS diet_logs (
    logID        INT AUTO_INCREMENT PRIMARY KEY,
    userID       INT NOT NULL,
    itemID       INT NOT NULL,
    timestamp    DATETIME NOT NULL,
    portionSize  FLOAT DEFAULT 1.0,
    CONSTRAINT fk_diet_user
        FOREIGN KEY (userID)
        REFERENCES users(userID)
        ON DELETE CASCADE,
    CONSTRAINT fk_diet_item
        FOREIGN KEY (itemID)
        REFERENCES menu_items(itemID)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 建立評論資料表
CREATE TABLE IF NOT EXISTS reviews (
    reviewID      INT AUTO_INCREMENT PRIMARY KEY,
    restaurantID  INT NOT NULL,
    userID        INT NOT NULL,
    rating        INT NOT NULL,
    comment       TEXT,
    timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_restaurant
        FOREIGN KEY (restaurantID)
        REFERENCES restaurants(restaurantID)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_user
        FOREIGN KEY (userID)
        REFERENCES users(userID)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 建議索引
CREATE INDEX idx_menu_restaurant    ON menu_items(restaurantID);
CREATE INDEX idx_diet_user_time     ON diet_logs(userID, timestamp);
CREATE INDEX idx_review_restaurant  ON reviews(restaurantID);
