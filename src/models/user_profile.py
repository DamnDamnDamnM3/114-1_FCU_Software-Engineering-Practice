"""
UserProfile 類別
使用者個人資料設定
"""

from dataclasses import dataclass
from typing import Optional
from .app_mode import AppMode
from .health_profile import HealthProfile


@dataclass
class UserProfile:
    """使用者個人資料"""
    budget: float                              # 預算
    mode: AppMode                               # 應用程式模式
    health_goal: Optional[HealthProfile] = None # 健康目標（可選，用於 FITNESS 模式）

    def __init__(self, budget: float = 0.0, mode: AppMode = AppMode.NORMAL, health_goal: Optional[HealthProfile] = None):
        self.budget = budget
        self.mode = mode
        self.health_goal = health_goal

    def set_budget(self, amount: float) -> None:
        """設定預算"""
        self.budget = amount

    def set_mode(self, mode: AppMode) -> None:
        """設定應用程式模式"""
        self.mode = mode

    def set_health_goal(self, goal: HealthProfile) -> None:
        """設定健康目標"""
        self.health_goal = goal
