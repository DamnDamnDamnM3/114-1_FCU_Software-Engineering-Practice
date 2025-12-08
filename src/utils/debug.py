"""
條件輸出工具模組
類似 C/C++ 的 #ifdef，用於控制程式訊息的輸出

使用方式：
    from utils.debug import DEBUG_PRINT, WARN_PRINT, ERROR_PRINT

    DEBUG_PRINT("這是一個除錯訊息")
    WARN_PRINT("這是一個警告訊息")
    ERROR_PRINT("這是一個錯誤訊息")

環境變數控制：
    DEBUG_MODE=1     # 啟用除錯訊息輸出
    VERBOSE_MODE=1   # 啟用詳細訊息輸出（包含 INFO）
"""

import os
import sys
from typing import Any


def _get_env_bool(key: str, default: bool = False) -> bool:
    """從環境變數讀取布林值"""
    value = os.getenv(key, "").lower()
    return value in ("1", "true", "yes", "on", "enabled")


# 讀取環境變數設定
_DEBUG_ENABLED = _get_env_bool("DEBUG_MODE", default=False)
_VERBOSE_ENABLED = _get_env_bool("VERBOSE_MODE", default=False)


def is_debug_enabled() -> bool:
    """檢查是否啟用除錯模式"""
    return _DEBUG_ENABLED


def is_verbose_enabled() -> bool:
    """檢查是否啟用詳細模式"""
    return _VERBOSE_ENABLED


def DEBUG_PRINT(*args: Any, **kwargs: Any) -> None:
    """
    條件輸出除錯訊息
    只有在 DEBUG_MODE=1 時才會輸出
    """
    if _DEBUG_ENABLED:
        print(*args, **kwargs, file=sys.stderr)


def INFO_PRINT(*args: Any, **kwargs: Any) -> None:
    """
    條件輸出資訊訊息
    只有在 VERBOSE_MODE=1 或 DEBUG_MODE=1 時才會輸出
    """
    if _VERBOSE_ENABLED or _DEBUG_ENABLED:
        print(*args, **kwargs)


def WARN_PRINT(*args: Any, **kwargs: Any) -> None:
    """
    條件輸出警告訊息
    只有在 VERBOSE_MODE=1 或 DEBUG_MODE=1 時才會輸出
    """
    if _VERBOSE_ENABLED or _DEBUG_ENABLED:
        print(*args, **kwargs, file=sys.stderr)


def ERROR_PRINT(*args: Any, **kwargs: Any) -> None:
    """
    條件輸出錯誤訊息
    預設總是輸出（除非明確禁用）
    可以通過環境變數 ERROR_OUTPUT=0 來禁用
    """
    error_output = _get_env_bool("ERROR_OUTPUT", default=True)
    if error_output:
        print(*args, **kwargs, file=sys.stderr)

