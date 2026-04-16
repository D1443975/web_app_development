"""
Transaction Model — 收支紀錄模型
負責 transactions 資料表的 CRUD 操作與統計查詢
"""

import sqlite3
from datetime import datetime


class Transaction:
    """收支紀錄模型，對應 transactions 資料表"""

    def __init__(self, id=None, type=None, amount=None, category_id=None,
                 date=None, note='', created_at=None, updated_at=None):
        self.id = id
        self.type = type            # 'income' 或 'expense'
        self.amount = amount        # 金額（正數）
        self.category_id = category_id
        self.date = date            # 格式：YYYY-MM-DD
        self.note = note
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_db(db_path):
        """取得資料庫連線"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # =============================================
    # 基本 CRUD 操作
    # =============================================

    @staticmethod
    def create(db_path, type, amount, category_id, date, note=''):
        """新增一筆收支紀錄"""
        conn = Transaction.get_db(db_path)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.execute(
            """INSERT INTO transactions (type, amount, category_id, date, note, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (type, amount, category_id, date, note, now, now)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all(db_path):
        """取得所有收支紀錄（含類別名稱），依日期降序排列"""
        conn = Transaction.get_db(db_path)
        rows = conn.execute(
            """SELECT t.*, c.name AS category_name
               FROM transactions t
               LEFT JOIN categories c ON t.category_id = c.id
               ORDER BY t.date DESC, t.created_at DESC"""
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(db_path, transaction_id):
        """依 ID 取得單一收支紀錄（含類別名稱）"""
        conn = Transaction.get_db(db_path)
        row = conn.execute(
            """SELECT t.*, c.name AS category_name
               FROM transactions t
               LEFT JOIN categories c ON t.category_id = c.id
               WHERE t.id = ?""",
            (transaction_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(db_path, transaction_id, type, amount, category_id, date, note=''):
        """更新一筆收支紀錄"""
        conn = Transaction.get_db(db_path)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(
            """UPDATE transactions
               SET type = ?, amount = ?, category_id = ?, date = ?, note = ?, updated_at = ?
               WHERE id = ?""",
            (type, amount, category_id, date, note, now, transaction_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(db_path, transaction_id):
        """刪除一筆收支紀錄"""
        conn = Transaction.get_db(db_path)
        conn.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )
        conn.commit()
        conn.close()

    # =============================================
    # 統計查詢
    # =============================================

    @staticmethod
    def get_balance(db_path):
        """取得餘額統計：總收入、總支出、目前餘額"""
        conn = Transaction.get_db(db_path)

        row = conn.execute(
            """SELECT
                 COALESCE(SUM(CASE WHEN type = 'income'  THEN amount ELSE 0 END), 0) AS total_income,
                 COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS total_expense
               FROM transactions"""
        ).fetchone()

        conn.close()

        total_income = row['total_income']
        total_expense = row['total_expense']
        balance = total_income - total_expense

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance
        }

    @staticmethod
    def get_expense_by_category(db_path):
        """取得各類別的支出統計"""
        conn = Transaction.get_db(db_path)
        rows = conn.execute(
            """SELECT c.name AS category_name, SUM(t.amount) AS total_amount
               FROM transactions t
               LEFT JOIN categories c ON t.category_id = c.id
               WHERE t.type = 'expense'
               GROUP BY t.category_id
               ORDER BY total_amount DESC"""
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_income_by_category(db_path):
        """取得各類別的收入統計"""
        conn = Transaction.get_db(db_path)
        rows = conn.execute(
            """SELECT c.name AS category_name, SUM(t.amount) AS total_amount
               FROM transactions t
               LEFT JOIN categories c ON t.category_id = c.id
               WHERE t.type = 'income'
               GROUP BY t.category_id
               ORDER BY total_amount DESC"""
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_monthly_summary(db_path):
        """取得每月收支統計"""
        conn = Transaction.get_db(db_path)
        rows = conn.execute(
            """SELECT
                 strftime('%Y-%m', date) AS month,
                 COALESCE(SUM(CASE WHEN type = 'income'  THEN amount ELSE 0 END), 0) AS total_income,
                 COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS total_expense
               FROM transactions
               GROUP BY strftime('%Y-%m', date)
               ORDER BY month DESC"""
        ).fetchall()
        conn.close()

        result = []
        for row in rows:
            data = dict(row)
            data['balance'] = data['total_income'] - data['total_expense']
            result.append(data)

        return result
