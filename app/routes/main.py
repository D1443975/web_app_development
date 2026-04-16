"""
Main Routes — 首頁路由
Blueprint: main
負責首頁儀表板的顯示
"""

from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁儀表板

    - URL: GET /
    - 處理邏輯: 呼叫 Transaction.get_balance() 取得總收入、總支出、餘額
    - 輸出: 渲染 index.html，傳入 total_income, total_expense, balance
    """
    # TODO: 實作首頁邏輯
    pass
