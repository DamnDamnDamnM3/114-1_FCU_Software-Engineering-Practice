"""
AppMode 列舉
定義應用程式的使用模式
"""

from enum import Enum


class AppMode(Enum):
    """應用程式使用模式"""
    NORMAL = "NORMAL"      # 一般模式
    FITNESS = "FITNESS"    # 健身模式
    TOURIST = "TOURIST"    # 觀光模式
