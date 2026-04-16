"""
Transaction Routes — 收支紀錄路由
Blueprint: transaction
負責收支紀錄的 CRUD 操作（列表、新增、編輯、刪除）
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')


@transaction_bp.route('/')
def list_transactions():
    """
    收支紀錄列表

    - URL: GET /transactions
    - 處理邏輯: 呼叫 Transaction.get_all() 取得所有紀錄（含類別名稱）
    - 輸出: 渲染 transactions/list.html，傳入 transactions 列表
    """
    # TODO: 實作列表邏輯
    pass


@transaction_bp.route('/create', methods=['GET'])
def create_form():
    """
    新增紀錄頁面

    - URL: GET /transactions/create
    - 處理邏輯: 呼叫 Category.get_by_type() 取得收入與支出的類別選單
    - 輸出: 渲染 transactions/create.html，傳入 income_categories, expense_categories
    """
    # TODO: 實作新增表單頁面
    pass


@transaction_bp.route('/create', methods=['POST'])
def create_transaction():
    """
    建立紀錄

    - URL: POST /transactions/create
    - 輸入（表單欄位）: type, amount, category_id, date, note
    - 處理邏輯:
        1. 驗證輸入（type 有效、amount > 0、date 格式正確、category_id 存在）
        2. 呼叫 Transaction.create() 新增紀錄
    - 輸出:
        - 成功: 重導向至 /transactions
        - 失敗: 重新渲染 create.html，帶入錯誤訊息（flash）
    """
    # TODO: 實作新增邏輯
    pass


@transaction_bp.route('/<int:id>/edit', methods=['GET'])
def edit_form(id):
    """
    編輯紀錄頁面

    - URL: GET /transactions/<id>/edit
    - 輸入: URL 參數 id（紀錄 ID）
    - 處理邏輯:
        1. 呼叫 Transaction.get_by_id() 取得紀錄
        2. 呼叫 Category.get_by_type() 取得類別選單
    - 輸出: 渲染 transactions/edit.html，傳入 transaction 與類別列表
    - 錯誤處理: 紀錄不存在時返回 404
    """
    # TODO: 實作編輯表單頁面
    pass


@transaction_bp.route('/<int:id>/edit', methods=['POST'])
def update_transaction(id):
    """
    更新紀錄

    - URL: POST /transactions/<id>/edit
    - 輸入: URL 參數 id + 表單欄位（同新增）
    - 處理邏輯:
        1. 驗證輸入
        2. 呼叫 Transaction.update() 更新紀錄
    - 輸出:
        - 成功: 重導向至 /transactions
        - 失敗: 重新渲染 edit.html，帶入錯誤訊息（flash）
    - 錯誤處理: 紀錄不存在返回 404；驗證失敗用 flash() 顯示錯誤
    """
    # TODO: 實作更新邏輯
    pass


@transaction_bp.route('/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除紀錄

    - URL: POST /transactions/<id>/delete
    - 輸入: URL 參數 id（紀錄 ID）
    - 處理邏輯: 呼叫 Transaction.delete() 刪除紀錄
    - 輸出: 重導向至 /transactions
    - 錯誤處理: 紀錄不存在時返回 404
    """
    # TODO: 實作刪除邏輯
    pass
