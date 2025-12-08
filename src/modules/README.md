# 模組開發指南

## 目錄結構

每個模組應該遵循以下結構：

```
modules/
├── your_module/          # 你的模組名稱
│   ├── __init__.py      # 模組初始化，創建 Blueprint
│   └── routes.py        # 路由定義
└── ...
```

## 創建新模組的步驟

### 1. 創建模組資料夾

```bash
mkdir -p modules/your_module
```

### 2. 創建 `__init__.py`

```python
"""
Your Module 模組
模組描述
"""

from flask import Blueprint

# 創建 Blueprint
# url_prefix 是可選的，用於為所有路由添加前綴（例如 '/api'）
your_module_bp = Blueprint('your_module', __name__, url_prefix='')

# 導入路由（必須在 Blueprint 創建之後）
from . import routes
```

**重要：** Blueprint 變數名稱必須是 `{模組名}_bp`，例如模組名為 `user`，則變數名為 `user_bp`

### 3. 創建 `routes.py`

```python
"""
Your Module 模組的路由定義
"""

from flask import render_template, jsonify, request
from . import your_module_bp


@your_module_bp.route('/your-route')
def your_function():
    """路由描述"""
    return render_template('your_module/your_template.html')
    # 或返回 JSON
    # return jsonify({'message': 'Hello'})
```

### 4. 創建模板（如果需要）

如果模組需要 HTML 模板，在 `templates` 資料夾中創建對應的子資料夾：

```
templates/
└── your_module/
    └── your_template.html
```

## 範例：創建一個 User 模組

### 1. 目錄結構

```
modules/
└── user/
    ├── __init__.py
    └── routes.py
```

### 2. `modules/user/__init__.py`

```python
from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/auth')

from . import routes
```

### 3. `modules/user/routes.py`

```python
from flask import render_template, request, flash, redirect, url_for
from services.db import authenticate_user, DatabaseError
from . import user_bp


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        try:
            user = authenticate_user(username, password)
        except DatabaseError as exc:
            flash(str(exc), 'danger')
        else:
            if user:
                flash('登入成功', 'success')
                return redirect(url_for('home.index'))
            flash('帳號或密碼錯誤', 'danger')

    return render_template('user/login.html')
```

### 4. 模板（可選）

```
templates/
└── user/
    └── login.html
```

## 注意事項

1. **Blueprint 命名規則**：變數名必須是 `{模組名}_bp`
2. **自動載入**：主應用程式會自動掃描並載入所有模組，無需手動修改 `app.py`
3. **路由前綴**：可以在創建 Blueprint 時使用 `url_prefix` 參數為所有路由添加前綴
4. **模板路徑**：建議將模板放在 `templates/{模組名}/` 資料夾中，避免命名衝突

## 測試你的模組

1. 將模組放在 `modules/` 資料夾中
2. 運行應用程式：`python app.py`
3. 如果模組載入成功，會在終端看到：`[OK] 已載入模組: your_module`
4. 訪問你的路由測試功能

