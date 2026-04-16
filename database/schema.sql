-- ============================================
-- 個人記帳簿系統 — SQLite 資料庫 Schema
-- ============================================

-- 啟用外鍵約束
PRAGMA foreign_keys = ON;

-- -------------------------------------------
-- 類別表 (categories)
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL,
    type TEXT    NOT NULL CHECK (type IN ('income', 'expense'))
);

-- -------------------------------------------
-- 交易紀錄表 (transactions)
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    type        TEXT    NOT NULL CHECK (type IN ('income', 'expense')),
    amount      REAL    NOT NULL CHECK (amount > 0),
    category_id INTEGER NOT NULL,
    date        TEXT    NOT NULL,
    note        TEXT    DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- -------------------------------------------
-- 索引
-- -------------------------------------------
CREATE INDEX IF NOT EXISTS idx_transactions_date        ON transactions (date);
CREATE INDEX IF NOT EXISTS idx_transactions_type        ON transactions (type);
CREATE INDEX IF NOT EXISTS idx_transactions_category_id ON transactions (category_id);

-- -------------------------------------------
-- 預設類別資料
-- -------------------------------------------

-- 收入類別
INSERT OR IGNORE INTO categories (id, name, type) VALUES (1,  '薪資',     'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (2,  '獎金',     'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (3,  '投資收益', 'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (4,  '兼職',     'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (5,  '其他收入', 'income');

-- 支出類別
INSERT OR IGNORE INTO categories (id, name, type) VALUES (6,  '飲食',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (7,  '交通',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (8,  '住宿',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (9,  '娛樂',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (10, '購物',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (11, '醫療',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (12, '教育',     'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (13, '日用品',   'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (14, '其他支出', 'expense');
