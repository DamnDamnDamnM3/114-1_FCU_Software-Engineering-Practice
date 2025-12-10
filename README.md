# 114-1_FCU_Software-Engineering-Practice

Flask 模組化網頁應用程式專案

## 專案結構

```
.
├── ENV/                  # 環境變數資料夾
│   ├── .env             # 環境變數檔案（不提交到版本控制）
│   └── .env.example    # 環境變數範例檔案
├── docs/                # 文件資料夾
│   ├── Database_Schema.md # 資料庫結構文件
│   ├── Models_Implementation.md # 資料模型實作文件
│   └── Restaurant_API.md # Restaurant API 文件
├── src/
│   ├── app.py           # 主應用程式（自動載入所有模組）
│   ├── modules/         # 模組資料夾（每個開發者的模組放在這裡）
│   │   ├── home/       # 範例模組：首頁與靜態頁面
│   │   ├── user/       # 使用者登入模組（Blueprint: user_bp）
│   │   ├── restaurant/ # 餐廳搜尋/推薦/飲食記錄模組（Blueprint: restaurant_bp）
│   │   └── README.md   # 模組開發指南
│   ├── models/        # 資料模型（User, Restaurant, MenuItem 等）
│   ├── services/       # 共用服務（例如資料庫連線、搜尋、推薦）
│   ├── data/          # 範例資料
│   ├── templates/      # HTML 模板資料夾
│   │   ├── home/       # 各模組的模板（建議按模組分資料夾）
│   │   └── user/
│   ├── utils/          # 工具模組
│   │   └── debug.py    # 條件輸出工具（類似 #ifdef）
│   ├── scripts/        # 腳本資料夾
│   │   ├── init_db.py  # 資料庫初始化腳本
│   │   └── init_db.sql # 資料庫初始化 SQL
│   └── requirements.txt # Python 依賴套件
├── deploy.sh            # 部署腳本
└── run.sh               # 運行腳本
```

## 快速開始

### 方式一：使用自動部署腳本（推薦）

```bash
# 執行部署腳本（會自動安裝系統依賴和 Python 套件）
./deploy.sh
```

### 方式二：手動安裝

### 1. 安裝系統依賴（僅首次需要）

**Ubuntu 24.04:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv libmariadb-dev
```

### 2. 創建虛擬環境並安裝 Python 依賴

```bash
# 創建虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 安裝套件
pip install -r src/requirements.txt
```

### 3. 運行應用程式

```bash
# 使用提供的腳本運行（會自動啟動虛擬環境）
./run.sh

# 或手動運行
source venv/bin/activate
python3 src/app.py
```

應用程式將在 `http://localhost:5000` 啟動

### 4. 設定環境變數

```bash
# 編輯 ENV/.env 檔案，填入正確的資料庫帳號密碼與系統設定
nano ENV/.env
```

應用程式會自動從 `ENV/.env` 檔案載入環境變數。請參考 `ENV/.env.example` 檔案了解各項設定的說明。

## 模組化開發

此專案採用模組化架構，使用 Flask Blueprint 實現。每個開發者可以獨立開發自己的模組，無需修改主應用程式。

### 如何創建新模組

詳細說明請參考：[`src/modules/README.md`](src/modules/README.md)

**快速步驟：**

1. 在 `modules/` 資料夾中創建新資料夾（例如：`user`）
2. 創建 `__init__.py` 和 `routes.py`
3. 在 `__init__.py` 中創建 Blueprint（變數名必須是 `{模組名}_bp`）
4. 在 `routes.py` 中定義路由
5. 運行應用程式，模組會自動載入

### 範例模組

查看 `modules/home/` 與 `modules/user/` 作為參考範例。

### Restaurant API 模組

`modules/restaurant/` 模組提供完整的餐廳搜尋、推薦、飲食記錄和分析功能。

**主要功能：**
- 餐廳搜尋與列表
- 餐廳詳情與菜單
- 餐廳評論
- 個人化推薦
- 飲食記錄管理
- 飲食分析報告

詳細 API 文件請參考：[`docs/Restaurant_API.md`](docs/Restaurant_API.md)

## 開發規範

- 每個模組應該有獨立的資料夾
- Blueprint 變數命名：`{模組名}_bp`
- 模板建議放在 `templates/{模組名}/` 資料夾中
- 主應用程式會自動掃描並載入所有模組

## 使用者登入與資料庫安全

- 新增 `/auth/login` 路由（`user` 模組）提供登入介面
- 所有登入查詢透過 `services/db.py` 使用參數化查詢，防止 SQL Injection
- 密碼驗證採用 `werkzeug.security.check_password_hash`

### 資料庫環境變數

可透過 `ENV/.env` 檔案或環境變數設定 MariaDB 連線資訊：

| 變數        | 預設值    | 說明             |
|-------------|-----------|------------------|
| `SECRET_KEY` | dev-secret-key | Flask 密鑰（正式環境請更改） |
| `DB_HOST`   | 127.0.0.1 | 資料庫主機       |
| `DB_PORT`   | 3306      | 資料庫連接埠     |
| `DB_USER`   | root      | 使用者名稱       |
| `DB_PASSWORD` | 空字串  | 使用者密碼       |
| `DB_NAME`   | app_db    | 目標資料庫       |

**設定方式：**
1. 在 `ENV/` 資料夾中建立 `.env` 檔案（可參考 `ENV/.env.example`）
2. 編輯 `ENV/.env` 檔案填入正確的值
3. 應用程式會自動載入 `ENV/.env` 檔案中的設定

請於正式環境設置 `SECRET_KEY` 與上述資料庫參數。

### 資料庫初始化

在首次使用前，需要初始化資料庫結構：

**方式一：使用 Python 腳本（推薦）**

```bash
# 執行初始化腳本
python3 src/scripts/init_db.py

# 建立預設使用者（從 ENV/.env 讀取設定）
CREATE_DEFAULT_USER=1 python3 src/scripts/init_db.py
```

預設使用者資訊可在 `ENV/.env` 檔案中設定：
- `DEFAULT_USERNAME`: 預設使用者名稱（預設: admin）
- `DEFAULT_PASSWORD`: 預設密碼（預設: admin123）
- `DEFAULT_EMAIL`: 預設電子郵件（預設: admin@example.com）

**方式二：使用 SQL 腳本**

```bash
mysql -u root -p < src/scripts/init_db.sql
```

**方式三：手動執行 SQL**

參考 [`docs/Database_Schema.md`](docs/Database_Schema.md) 中的 SQL 語句手動執行。

詳細的資料庫結構說明請參考：[`docs/Database_Schema.md`](docs/Database_Schema.md)

### 程式訊息輸出控制（類似 #ifdef）

可透過環境變數控制程式訊息的輸出，類似 C/C++ 的 `#ifdef` 功能：

| 變數        | 預設值 | 說明             |
|-------------|--------|------------------|
| `DEBUG_MODE` | 0      | 啟用除錯訊息輸出（`DEBUG_PRINT`） |
| `VERBOSE_MODE` | 0    | 啟用詳細訊息輸出（`INFO_PRINT`, `WARN_PRINT`） |
| `ERROR_OUTPUT` | 1    | 錯誤訊息輸出（預設啟用） |

**使用方式：**

在程式碼中使用條件輸出函數：

```python
from utils.debug import DEBUG_PRINT, INFO_PRINT, WARN_PRINT, ERROR_PRINT

DEBUG_PRINT("這是一個除錯訊息")  # 只在 DEBUG_MODE=1 時輸出
INFO_PRINT("這是一個資訊訊息")   # 只在 VERBOSE_MODE=1 或 DEBUG_MODE=1 時輸出
WARN_PRINT("這是一個警告訊息")   # 只在 VERBOSE_MODE=1 或 DEBUG_MODE=1 時輸出
ERROR_PRINT("這是一個錯誤訊息")  # 預設總是輸出（除非 ERROR_OUTPUT=0）
```

在 `ENV/.env` 檔案中設定：

```bash
DEBUG_MODE=1      # 啟用除錯模式
VERBOSE_MODE=1    # 啟用詳細模式
ERROR_OUTPUT=1    # 啟用錯誤輸出（預設）
```

## 技術棧

- Python 3.x
- Flask >= 3.0.0
- mariadb >= 1.1.10
