"""
Category Model — 類別模型
負責 categories 資料表的 CRUD 操作
"""

import sqlite3


class Category:
    """類別模型，對應 categories 資料表"""

    def __init__(self, id=None, name=None, type=None):
        self.id = id
        self.name = name
        self.type = type  # 'income' 或 'expense'

    @staticmethod
    def get_db(db_path):
        """取得資料庫連線"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ----- 查詢 -----

    @staticmethod
    def get_all(db_path):
        """取得所有類別"""
        conn = Category.get_db(db_path)
        rows = conn.execute(
            "SELECT * FROM categories ORDER BY type, id"
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(db_path, category_id):
        """依 ID 取得單一類別"""
        conn = Category.get_db(db_path)
        row = conn.execute(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_type(db_path, category_type):
        """依類型取得類別列表（income 或 expense）"""
        conn = Category.get_db(db_path)
        rows = conn.execute(
            "SELECT * FROM categories WHERE type = ? ORDER BY id",
            (category_type,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ----- 新增 -----

    @staticmethod
    def create(db_path, name, category_type):
        """新增一個類別"""
        conn = Category.get_db(db_path)
        cursor = conn.execute(
            "INSERT INTO categories (name, type) VALUES (?, ?)",
            (name, category_type)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    # ----- 更新 -----

    @staticmethod
    def update(db_path, category_id, name, category_type):
        """更新類別資料"""
        conn = Category.get_db(db_path)
        conn.execute(
            "UPDATE categories SET name = ?, type = ? WHERE id = ?",
            (name, category_type, category_id)
        )
        conn.commit()
        conn.close()

    # ----- 刪除 -----

    @staticmethod
    def delete(db_path, category_id):
        """刪除類別"""
        conn = Category.get_db(db_path)
        conn.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )
        conn.commit()
        conn.close()
