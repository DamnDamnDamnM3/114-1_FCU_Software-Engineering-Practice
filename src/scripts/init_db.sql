-- 資料庫初始化 SQL 腳本
-- 用於建立資料庫表格與欄位

-- 建立資料庫（如果不存在）
CREATE DATABASE IF NOT EXISTS `app_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用資料庫
USE `app_db`;

-- 建立 users 資料表
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '使用者 ID',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '使用者名稱',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密碼雜湊值',
    `email` VARCHAR(100) COMMENT '電子郵件',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '建立時間',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
    INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='使用者資料表';

