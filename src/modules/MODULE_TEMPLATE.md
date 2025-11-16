# 模組模板

複製此模板來快速創建新模組：

## 快速開始

1. 複製 `home` 模組作為模板
2. 重命名資料夾為你的模組名稱
3. 修改 `__init__.py` 中的 Blueprint 名稱
4. 在 `routes.py` 中添加你的路由

## 最小化模組結構

```
your_module/
├── __init__.py
└── routes.py
```

### `__init__.py` 模板

```python
"""
Your Module 模組
模組描述
"""

from flask import Blueprint

# 創建 Blueprint
your_module_bp = Blueprint('your_module', __name__, url_prefix='')

# 導入路由
from . import routes
```

### `routes.py` 模板

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
```

