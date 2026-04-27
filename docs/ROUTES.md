# 路由與頁面設計文件：食譜收藏系統

根據 PRD 與系統架構文件，本文件規劃了所有的 Flask 路由、HTTP 方法、處理邏輯與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/所有食譜** | GET | `/` | `recipe/index.html` | 顯示最新或所有的公開食譜列表 |
| **搜尋食譜** | GET | `/search` | `recipe/index.html` | 透過 `?q=關鍵字` 搜尋食譜 |
| **註冊頁面** | GET | `/register` | `auth/register.html` | 顯示使用者註冊表單 |
| **處理註冊** | POST | `/register` | — | 接收註冊資料，寫入 DB，重導向至登入頁 |
| **登入頁面** | GET | `/login` | `auth/login.html` | 顯示登入表單 |
| **處理登入** | POST | `/login` | — | 驗證密碼，設定 Session，重導向至首頁 |
| **使用者登出** | GET | `/logout` | — | 清除 Session 並重導向至首頁 |
| **新增食譜頁面** | GET | `/recipe/create` | `recipe/create.html` | 顯示新增食譜表單 (需登入) |
| **處理新增食譜** | POST | `/recipe/create` | — | 寫入食譜，重導向至該食譜詳細頁 |
| **食譜詳細頁** | GET | `/recipe/<id>` | `recipe/detail.html` | 顯示食譜完整內容、食材與作法 |
| **編輯食譜頁面** | GET | `/recipe/<id>/edit`| `recipe/edit.html` | 顯示編輯表單 (需為擁有者或管理員) |
| **處理更新食譜** | POST | `/recipe/<id>/update`| — | 更新食譜資料，重導向至食譜詳細頁 |
| **刪除食譜** | POST | `/recipe/<id>/delete`| — | 刪除食譜，重導向至首頁 (需權限) |
| **收藏/取消收藏** | POST | `/recipe/<id>/collect`| — | 切換收藏狀態，並重導向回原頁面或詳細頁 |
| **我的收藏** | GET | `/my_collection` | `recipe/my_collection.html` | 顯示使用者已收藏的食譜清單 |

---

## 2. 每個路由的詳細說明

### 認證相關 (Auth Routes)

- **`GET /register`**
  - **輸出**：渲染 `auth/register.html`。
- **`POST /register`**
  - **輸入**：表單欄位 `username`, `password`。
  - **處理邏輯**：驗證 username 是否已存在，將密碼雜湊，呼叫 `User.create()`。
  - **輸出**：成功則重導向 `/login`，失敗則顯示錯誤訊息於原註冊頁。
- **`GET /login`**
  - **輸出**：渲染 `auth/login.html`。
- **`POST /login`**
  - **輸入**：表單欄位 `username`, `password`。
  - **處理邏輯**：查詢使用者，驗證密碼，若正確則寫入 `session['user_id']`。
  - **輸出**：成功則重導向 `/`，失敗則顯示錯誤訊息於原登入頁。
- **`GET /logout`**
  - **處理邏輯**：清除 `session.clear()`。
  - **輸出**：重導向 `/`。

### 食譜相關 (Recipe Routes)

- **`GET /` 及 `GET /search`**
  - **輸入**：(可選) URL 參數 `?q=keyword`。
  - **處理邏輯**：若有 keyword，呼叫 `Recipe.search(keyword)`；否則呼叫 `Recipe.get_all()`。
  - **輸出**：將食譜列表傳給 `recipe/index.html` 渲染。
- **`GET /recipe/create`**
  - **邏輯**：檢查是否登入，未登入重導向 `/login`。
  - **輸出**：渲染 `recipe/create.html`。
- **`POST /recipe/create`**
  - **輸入**：表單 `title`, `description`, `ingredients`, `instructions`。
  - **處理邏輯**：呼叫 `Recipe.create()`，取得新 `id`。
  - **輸出**：重導向 `/recipe/<id>`。
- **`GET /recipe/<id>`**
  - **輸入**：URL 路徑 `id`。
  - **處理邏輯**：呼叫 `Recipe.get_by_id(id)`，並檢查當前使用者是否已收藏。如果找不到食譜回傳 404。
  - **輸出**：渲染 `recipe/detail.html`。
- **`GET /recipe/<id>/edit`**
  - **邏輯**：檢查登入及權限 (是否為作者或 admin)。
  - **輸出**：帶入舊資料渲染 `recipe/edit.html`。
- **`POST /recipe/<id>/update`**
  - **輸入**：表單更新資料。
  - **處理邏輯**：檢查權限，呼叫 `Recipe.update()`。
  - **輸出**：重導向 `/recipe/<id>`。
- **`POST /recipe/<id>/delete`**
  - **邏輯**：檢查權限，呼叫 `Recipe.delete()`。
  - **輸出**：重導向 `/`。
- **`POST /recipe/<id>/collect`**
  - **邏輯**：檢查是否登入。呼叫 `Collection.is_collected()` 判斷後，執行 `add()` 或 `remove()`。
  - **輸出**：重導向回上一頁 (`request.referrer`) 或詳細頁。
- **`GET /my_collection`**
  - **邏輯**：檢查登入，呼叫 `Collection.get_user_collections(session['user_id'])`。
  - **輸出**：渲染 `recipe/my_collection.html`。

---

## 3. Jinja2 模板清單

所有模板皆繼承自 `base.html`，以保持共用的導覽列與外觀。

- `base.html` (共用外框：Header, Footer, Flash 訊息顯示)
- **`auth/`** (認證資料夾)
  - `register.html` (註冊表單)
  - `login.html` (登入表單)
- **`recipe/`** (食譜資料夾)
  - `index.html` (首頁/搜尋結果/列表)
  - `detail.html` (食譜詳細內容)
  - `create.html` (新增食譜表單)
  - `edit.html` (編輯食譜表單)
  - `my_collection.html` (我的收藏清單)
