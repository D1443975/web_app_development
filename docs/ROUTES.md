# 路由設計文件 — 個人記帳簿系統

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁儀表板 | GET | `/` | `templates/index.html` | 顯示總收入、總支出、目前餘額 |
| 收支紀錄列表 | GET | `/transactions` | `templates/transactions/list.html` | 顯示所有收支紀錄，依日期降序 |
| 新增紀錄頁面 | GET | `/transactions/create` | `templates/transactions/create.html` | 顯示新增收支紀錄表單 |
| 建立紀錄 | POST | `/transactions/create` | — | 接收表單，存入 DB，重導向至列表頁 |
| 編輯紀錄頁面 | GET | `/transactions/<id>/edit` | `templates/transactions/edit.html` | 顯示編輯表單，預填現有資料 |
| 更新紀錄 | POST | `/transactions/<id>/edit` | — | 接收表單，更新 DB，重導向至列表頁 |
| 刪除紀錄 | POST | `/transactions/<id>/delete` | — | 刪除紀錄後重導向至列表頁 |
| 類別統計 | GET | `/reports/category` | `templates/reports/category.html` | 顯示各類別支出金額統計 |
| 月度統計 | GET | `/reports/monthly` | `templates/reports/monthly.html` | 顯示每月收入、支出與結餘 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁儀表板

| 項目 | 內容 |
|------|------|
| **URL** | `GET /` |
| **Blueprint** | `main` |
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `Transaction.get_balance(db_path)` 取得總收入、總支出、餘額 |
| **輸出** | 渲染 `index.html`，傳入 `total_income`、`total_expense`、`balance` |
| **錯誤處理** | 無特殊處理 |

---

### 2.2 收支紀錄列表

| 項目 | 內容 |
|------|------|
| **URL** | `GET /transactions` |
| **Blueprint** | `transaction` |
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `Transaction.get_all(db_path)` 取得所有紀錄（含類別名稱） |
| **輸出** | 渲染 `transactions/list.html`，傳入 `transactions` 列表 |
| **錯誤處理** | 無特殊處理 |

---

### 2.3 新增紀錄頁面

| 項目 | 內容 |
|------|------|
| **URL** | `GET /transactions/create` |
| **Blueprint** | `transaction` |
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `Category.get_by_type(db_path, 'income')` 與 `Category.get_by_type(db_path, 'expense')` 取得類別選單 |
| **輸出** | 渲染 `transactions/create.html`，傳入 `income_categories`、`expense_categories` |
| **錯誤處理** | 無特殊處理 |

---

### 2.4 建立紀錄

| 項目 | 內容 |
|------|------|
| **URL** | `POST /transactions/create` |
| **Blueprint** | `transaction` |
| **輸入（表單欄位）** | `type`（income/expense）、`amount`（金額）、`category_id`（類別 ID）、`date`（日期）、`note`（備註） |
| **處理邏輯** | 1. 驗證輸入（type 有效、amount > 0、date 格式正確、category_id 存在）<br/>2. 呼叫 `Transaction.create(db_path, type, amount, category_id, date, note)` |
| **輸出** | 成功：重導向至 `/transactions`<br/>失敗：重新渲染 `create.html`，帶入錯誤訊息 |
| **錯誤處理** | 驗證失敗時，用 `flash()` 顯示錯誤訊息並返回表單頁 |

---

### 2.5 編輯紀錄頁面

| 項目 | 內容 |
|------|------|
| **URL** | `GET /transactions/<id>/edit` |
| **Blueprint** | `transaction` |
| **輸入** | URL 參數 `id`（紀錄 ID） |
| **處理邏輯** | 1. 呼叫 `Transaction.get_by_id(db_path, id)` 取得紀錄<br/>2. 呼叫 `Category.get_by_type()` 取得類別選單 |
| **輸出** | 渲染 `transactions/edit.html`，傳入 `transaction` 與類別列表 |
| **錯誤處理** | 紀錄不存在時返回 404 頁面 |

---

### 2.6 更新紀錄

| 項目 | 內容 |
|------|------|
| **URL** | `POST /transactions/<id>/edit` |
| **Blueprint** | `transaction` |
| **輸入** | URL 參數 `id` + 表單欄位（同新增） |
| **處理邏輯** | 1. 驗證輸入<br/>2. 呼叫 `Transaction.update(db_path, id, type, amount, category_id, date, note)` |
| **輸出** | 成功：重導向至 `/transactions`<br/>失敗：重新渲染 `edit.html`，帶入錯誤訊息 |
| **錯誤處理** | 紀錄不存在返回 404；驗證失敗用 `flash()` 顯示錯誤 |

---

### 2.7 刪除紀錄

| 項目 | 內容 |
|------|------|
| **URL** | `POST /transactions/<id>/delete` |
| **Blueprint** | `transaction` |
| **輸入** | URL 參數 `id`（紀錄 ID） |
| **處理邏輯** | 呼叫 `Transaction.delete(db_path, id)` |
| **輸出** | 重導向至 `/transactions` |
| **錯誤處理** | 紀錄不存在時返回 404 頁面 |

---

### 2.8 類別統計

| 項目 | 內容 |
|------|------|
| **URL** | `GET /reports/category` |
| **Blueprint** | `report` |
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `Transaction.get_expense_by_category(db_path)` 與 `Transaction.get_income_by_category(db_path)` |
| **輸出** | 渲染 `reports/category.html`，傳入 `expense_stats`、`income_stats` |
| **錯誤處理** | 無特殊處理 |

---

### 2.9 月度統計

| 項目 | 內容 |
|------|------|
| **URL** | `GET /reports/monthly` |
| **Blueprint** | `report` |
| **輸入** | 無 |
| **處理邏輯** | 呼叫 `Transaction.get_monthly_summary(db_path)` |
| **輸出** | 渲染 `reports/monthly.html`，傳入 `monthly_data` |
| **錯誤處理** | 無特殊處理 |

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承 | 用途 |
|----------|------|------|
| `templates/base.html` | — | 基底模板：共用 HTML 結構、導覽列、頁尾、CSS/JS 引入 |
| `templates/index.html` | `base.html` | 首頁儀表板：餘額總覽 |
| `templates/transactions/list.html` | `base.html` | 收支紀錄列表：所有紀錄的表格顯示 |
| `templates/transactions/create.html` | `base.html` | 新增紀錄表單：類型切換、類別選單、金額/日期/備註欄位 |
| `templates/transactions/edit.html` | `base.html` | 編輯紀錄表單：預填現有資料，結構同 create.html |
| `templates/reports/category.html` | `base.html` | 類別統計頁：各類別花費金額列表 |
| `templates/reports/monthly.html` | `base.html` | 月度統計頁：每月收入/支出/結餘列表 |

### 模板繼承結構

```
base.html
├── index.html
├── transactions/
│   ├── list.html
│   ├── create.html
│   └── edit.html
└── reports/
    ├── category.html
    └── monthly.html
```

---

> 📌 **文件版本**：v1.0  
> 📅 **建立日期**：2026-04-16  
> ✏️ **最後更新**：2026-04-16
