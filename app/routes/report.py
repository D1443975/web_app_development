"""
Report Routes — 統計報表路由
Blueprint: report
負責類別統計與月度統計的顯示
"""

from flask import Blueprint, render_template, current_app

report_bp = Blueprint('report', __name__, url_prefix='/reports')


@report_bp.route('/category')
def category_report():
    """
    類別統計

    - URL: GET /reports/category
    - 處理邏輯:
        1. 呼叫 Transaction.get_expense_by_category() 取得各類別支出統計
        2. 呼叫 Transaction.get_income_by_category() 取得各類別收入統計
    - 輸出: 渲染 reports/category.html，傳入 expense_stats, income_stats
    """
    # TODO: 實作類別統計邏輯
    pass


@report_bp.route('/monthly')
def monthly_report():
    """
    月度統計

    - URL: GET /reports/monthly
    - 處理邏輯: 呼叫 Transaction.get_monthly_summary() 取得每月收支統計
    - 輸出: 渲染 reports/monthly.html，傳入 monthly_data
    """
    # TODO: 實作月度統計邏輯
    pass
