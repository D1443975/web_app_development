# 流程圖文件 — 個人記帳簿系統

---

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    A([🌐 使用者開啟網頁]) --> B["🏠 首頁 - 儀表板<br/>顯示餘額總覽"]

    B --> C{"要執行什麼操作？"}

    C -->|新增收支| D["📝 新增紀錄頁"]
    C -->|查看紀錄| H["📋 收支紀錄列表"]
    C -->|查看統計| L{"查看哪種統計？"}

    %% 新增收支流程
    D --> E{"選擇類型"}
    E -->|收入| F1["選擇收入類別<br/>填寫金額/日期/備註"]
    E -->|支出| F2["選擇支出類別<br/>填寫金額/日期/備註"]
    F1 --> G["✅ 送出表單"]
    F2 --> G
    G --> G1{"驗證是否通過？"}
    G1 -->|通過| B
    G1 -->|失敗| D

    %% 收支紀錄列表流程
    H --> I{"要執行什麼操作？"}
    I -->|編輯| J["✏️ 編輯紀錄頁<br/>修改金額/類別/日期/備註"]
    I -->|刪除| K["🗑️ 確認刪除"]
    I -->|返回首頁| B
    J --> J1["💾 儲存修改"]
    J1 --> H
    K --> K1{"確認刪除？"}
    K1 -->|是| H
    K1 -->|否| H

    %% 統計報表流程
    L -->|類別統計| M["📊 類別花費統計頁<br/>各類別支出金額與比例"]
    L -->|月度統計| N["📅 月度花費統計頁<br/>每月收入/支出/結餘"]
    M --> B
    N --> B
```

### 流程說明

| 步驟 | 說明 |
|------|------|
| **進入首頁** | 使用者開啟網頁後，首頁顯示總收入、總支出與目前餘額 |
| **新增收支** | 選擇收入或支出，填寫類別、金額、日期與備註後送出 |
| **查看紀錄** | 瀏覽所有收支紀錄列表，可進一步編輯或刪除 |
| **編輯紀錄** | 修改已存在的收支紀錄內容，儲存後返回列表 |
| **刪除紀錄** | 點擊刪除後需確認，確認後從列表移除 |
| **類別統計** | 查看各類別的支出金額彙整 |
| **月度統計** | 查看每月的收入、支出與結餘變化 |

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增收支紀錄

描述使用者新增一筆收支紀錄時，資料從瀏覽器到資料庫的完整流程。

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Route as 🎮 Flask Route<br/>transaction.py
    participant Model as 📊 Model<br/>transaction.py
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「新增紀錄」
    Browser->>Route: GET /transactions/create
    Route->>Model: 取得所有類別
    Model->>DB: SELECT * FROM categories
    DB-->>Model: 類別列表
    Model-->>Route: 類別資料
    Route-->>Browser: 渲染 create.html（含類別選單）

    User->>Browser: 填寫表單並送出
    Browser->>Route: POST /transactions/create
    Route->>Route: 驗證輸入資料
    alt 驗證通過
        Route->>Model: 新增紀錄
        Model->>DB: INSERT INTO transactions
        DB-->>Model: 成功
        Model-->>Route: 新增完成
        Route-->>Browser: 重導向至首頁（302）
        Browser-->>User: 顯示首頁（餘額已更新）
    else 驗證失敗
        Route-->>Browser: 重新渲染 create.html（含錯誤訊息）
        Browser-->>User: 顯示錯誤提示
    end
```

### 2.2 查看首頁餘額

描述使用者進入首頁時，系統如何計算並顯示餘額。

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Route as 🎮 Flask Route<br/>main.py
    participant Model as 📊 Model<br/>transaction.py
    participant DB as 🗄️ SQLite

    User->>Browser: 開啟首頁
    Browser->>Route: GET /
    Route->>Model: 取得總收入
    Model->>DB: SELECT SUM(amount) FROM transactions WHERE type='income'
    DB-->>Model: 總收入金額
    Route->>Model: 取得總支出
    Model->>DB: SELECT SUM(amount) FROM transactions WHERE type='expense'
    DB-->>Model: 總支出金額
    Model-->>Route: 收入與支出數據
    Route->>Route: 計算餘額 = 總收入 − 總支出
    Route-->>Browser: 渲染 index.html（含餘額資訊）
    Browser-->>User: 顯示儀表板
```

### 2.3 編輯收支紀錄

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Route as 🎮 Flask Route<br/>transaction.py
    participant Model as 📊 Model<br/>transaction.py
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「編輯」按鈕
    Browser->>Route: GET /transactions/<id>/edit
    Route->>Model: 取得該筆紀錄
    Model->>DB: SELECT * FROM transactions WHERE id=?
    DB-->>Model: 紀錄資料
    Route->>Model: 取得所有類別
    Model->>DB: SELECT * FROM categories
    DB-->>Model: 類別列表
    Model-->>Route: 紀錄 + 類別資料
    Route-->>Browser: 渲染 edit.html（表單預填資料）

    User->>Browser: 修改內容並送出
    Browser->>Route: POST /transactions/<id>/edit
    Route->>Route: 驗證輸入資料
    alt 驗證通過
        Route->>Model: 更新紀錄
        Model->>DB: UPDATE transactions SET ... WHERE id=?
        DB-->>Model: 成功
        Model-->>Route: 更新完成
        Route-->>Browser: 重導向至紀錄列表（302）
        Browser-->>User: 顯示更新後的列表
    else 驗證失敗
        Route-->>Browser: 重新渲染 edit.html（含錯誤訊息）
        Browser-->>User: 顯示錯誤提示
    end
```

### 2.4 刪除收支紀錄

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Route as 🎮 Flask Route<br/>transaction.py
    participant Model as 📊 Model<br/>transaction.py
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser->>Route: POST /transactions/<id>/delete
    Route->>Model: 刪除紀錄
    Model->>DB: DELETE FROM transactions WHERE id=?
    DB-->>Model: 成功
    Model-->>Route: 刪除完成
    Route-->>Browser: 重導向至紀錄列表（302）
    Browser-->>User: 顯示更新後的列表
```

### 2.5 類別統計

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Route as 🎮 Flask Route<br/>report.py
    participant Model as 📊 Model<br/>transaction.py
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「類別統計」
    Browser->>Route: GET /reports/category
    Route->>Model: 取得各類別花費統計
    Model->>DB: SELECT category, SUM(amount) FROM transactions<br/>WHERE type='expense' GROUP BY category
    DB-->>Model: 各類別統計結果
    Model-->>Route: 統計資料
    Route-->>Browser: 渲染 category.html
    Browser-->>User: 顯示類別花費統計
```

### 2.6 月度統計

```mermaid
sequenceDiagram
    actor User as 👤 使用者
    participant Browser as 🌐 瀏覽器
    participant Route as 🎮 Flask Route<br/>report.py
    participant Model as 📊 Model<br/>transaction.py
    participant DB as 🗄️ SQLite

    User->>Browser: 點擊「月度統計」
    Browser->>Route: GET /reports/monthly
    Route->>Model: 取得每月收支統計
    Model->>DB: SELECT strftime('%Y-%m', date), type, SUM(amount)<br/>FROM transactions GROUP BY month, type
    DB-->>Model: 月度統計結果
    Model-->>Route: 統計資料
    Route-->>Browser: 渲染 monthly.html
    Browser-->>User: 顯示月度花費統計
```

---

## 3. 功能清單對照表

| 功能編號 | 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|----------|----------|----------|-----------|------|
| F3 | 首頁儀表板 | `/` | `GET` | 顯示總收入、總支出、目前餘額 |
| F1, F2 | 新增紀錄頁面 | `/transactions/create` | `GET` | 顯示新增收支紀錄表單 |
| F1, F2 | 新增紀錄送出 | `/transactions/create` | `POST` | 處理表單送出，寫入資料庫 |
| F6 | 收支紀錄列表 | `/transactions` | `GET` | 顯示所有收支紀錄，依日期排序 |
| F7 | 編輯紀錄頁面 | `/transactions/<id>/edit` | `GET` | 顯示編輯表單，預填現有資料 |
| F7 | 編輯紀錄送出 | `/transactions/<id>/edit` | `POST` | 處理編輯表單送出，更新資料庫 |
| F7 | 刪除紀錄 | `/transactions/<id>/delete` | `POST` | 刪除指定紀錄 |
| F4 | 類別統計 | `/reports/category` | `GET` | 顯示各類別支出金額統計 |
| F5 | 月度統計 | `/reports/monthly` | `GET` | 顯示每月收入、支出與結餘 |

---

> 📌 **文件版本**：v1.0  
> 📅 **建立日期**：2026-04-16  
> ✏️ **最後更新**：2026-04-16
