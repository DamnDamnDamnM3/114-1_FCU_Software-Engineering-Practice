# 114-1_FCU_Software-Engineering-Practice

Flask 模組化網頁應用程式專案

## 專案結構

```
src/
├── app.py                 # 主應用程式（自動載入所有模組）
├── modules/               # 模組資料夾（每個開發者的模組放在這裡）
│   ├── home/             # 範例模組：首頁和關於頁面
│   │   ├── __init__.py
│   │   └── routes.py
│   └── README.md         # 模組開發指南
├── templates/            # HTML 模板資料夾
│   └── home/            # 各模組的模板（建議按模組分資料夾）
└── requirements.txt      # Python 依賴套件
```

## 快速開始

### 1. 安裝依賴

```bash
# 啟動虛擬環境
source venv/bin/activate

# 安裝套件
pip install -r src/requirements.txt
```

### 2. 運行應用程式

```bash
cd src
python app.py
```

應用程式將在 `http://localhost:5000` 啟動

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

查看 `modules/home/` 作為參考範例。

## 開發規範

- 每個模組應該有獨立的資料夾
- Blueprint 變數命名：`{模組名}_bp`
- 模板建議放在 `templates/{模組名}/` 資料夾中
- 主應用程式會自動掃描並載入所有模組

## 技術棧

- Python 3.x
- Flask >= 3.0.0
