# 114-1_FCU_Software-Engineering-Practice

Flask 模組化網頁應用程式專案

## 專案結構

```
.
├── ENV/                  # 環境變數資料夾（需自行建立）
│   ├── .env             # 環境變數檔案（不提交到版本控制）
│   └── .env.example    # 環境變數範例檔案
├── dataset/             # 資料集資料夾
│   ├── restaurants.csv  # 餐廳資料 CSV 檔案
│   ├── menu_items.csv   # 餐點資料 CSV 檔案
│   └── app.py           # 資料生成腳本
├── docs/                # 文件資料夾
│   ├── Database_Schema.md # 資料庫結構文件
│   ├── Models_Implementation.md # 資料模型實作文件
│   ├── Restaurant_API.md # Restaurant API 文件
│   ├── Class Diagram.jpg # 類別圖
│   └── Use Case Diagram.jpg # 使用案例圖
├── sql/                 # SQL 腳本資料夾
│   ├── 001_create_tables.sql # 建立資料表 SQL
│   ├── 002_insert_sample_data.sql # 插入範例資料 SQL
│   └── SQL.sh           # SQL 執行腳本
├── src/
│   ├── app.py           # 主應用程式（自動載入所有模組）
│   ├── modules/         # 模組資料夾（每個開發者的模組放在這裡）
│   │   └── frontend/   # 前端模組（Blueprint: frontend_bp）
│   ├── services/        # 共用服務
│   │   └── db.py        # 資料庫連線服務
│   └── templates/       # HTML 模板資料夾
│       └── frontend/   # 前端模組的模板
└── requirements.txt     # Python 依賴套件（需在專案根目錄建立）
```

**注意：** 以下目錄為計劃中或程式碼引用但尚未建立：
- `src/models/` - 資料模型（程式碼中有引用，需建立）
- `src/data/` - 範例資料（程式碼中有引用，需建立）
- `src/utils/` - 工具模組（程式碼中有引用，需建立）
- `src/scripts/` - 腳本資料夾（可選）

## 快速開始

### 1. 安裝系統依賴

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

# 安裝套件（如果專案根目錄有 requirements.txt）
# 或手動安裝必要套件：
pip install flask python-dotenv mariadb

# 如果程式碼中引用了其他模組（models, data, utils），需要先建立這些目錄
```

### 3. 運行應用程式

```bash
# 啟動虛擬環境
source venv/bin/activate

# 運行應用程式
python3 src/app.py
```

應用程式將在 `http://localhost:5000` 啟動

### 4. 設定環境變數

```bash
# 建立 ENV 資料夾（如果不存在）
mkdir -p ENV

# 建立 .env 檔案，填入正確的資料庫帳號密碼與系統設定
nano ENV/.env
```

應用程式會自動從 `ENV/.env` 檔案載入環境變數。如果檔案不存在，應用程式會使用預設值。

**範例 .env 檔案內容：**
```bash
SECRET_KEY=your-secret-key-here
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=data
DEBUG_MODE=0
VERBOSE_MODE=0
ERROR_OUTPUT=1
```

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

### 現有模組

- **frontend 模組** (`src/modules/frontend/`): 前端頁面模組，提供餐廳搜尋、列表、詳情等功能
  - Blueprint: `frontend_bp`
  - 模板位置: `src/templates/frontend/`

### 參考文件

詳細的 API 和功能說明請參考：
- [`docs/Restaurant_API.md`](docs/Restaurant_API.md) - Restaurant API 文件
- [`docs/Models_Implementation.md`](docs/Models_Implementation.md) - 資料模型實作文件

## 開發規範

- 每個模組應該有獨立的資料夾
- Blueprint 變數命名：`{模組名}_bp`
- 模板建議放在 `templates/{模組名}/` 資料夾中
- 主應用程式會自動掃描並載入所有模組

## 資料庫安全

- 所有資料庫查詢透過 `services/db.py` 使用參數化查詢，防止 SQL Injection
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
| `DB_NAME`   | data      | 目標資料庫（與 SQL 腳本對齊） |

**設定方式：**
1. 在 `ENV/` 資料夾中建立 `.env` 檔案（可參考 `ENV/.env.example`）
2. 編輯 `ENV/.env` 檔案填入正確的值
3. 應用程式會自動載入 `ENV/.env` 檔案中的設定

請於正式環境設置 `SECRET_KEY` 與上述資料庫參數。

### 資料庫初始化

在首次使用前，需要初始化資料庫結構：

**方式一：使用 SQL 腳本（推薦）**

```bash
# 使用提供的 SQL.sh 腳本執行
cd sql
bash SQL.sh

# 或手動執行 SQL 腳本
mysql -P 3306 -u user -p data < 001_create_tables.sql
mysql -P 3306 -u user -p data < 002_insert_sample_data.sql
```

**方式二：使用 MySQL 客戶端手動執行**

```bash
# 連線到 MySQL
mysql -u root -p

# 在 MySQL 中執行
source sql/001_create_tables.sql
source sql/002_insert_sample_data.sql
```

**方式三：參考文件手動執行**

參考 [`docs/Database_Schema.md`](docs/Database_Schema.md) 中的 SQL 語句手動執行。

**注意：** SQL 腳本使用的資料庫名稱為 `data`，請確保資料庫已建立或修改腳本中的資料庫名稱。

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
