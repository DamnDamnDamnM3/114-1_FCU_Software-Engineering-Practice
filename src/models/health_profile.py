"""
HealthProfile 類別
用於當使用者 AppMode = FITNESS 時的健身目標設定
"""

from dataclasses import dataclass


@dataclass
class HealthProfile:
    """健康目標設定"""
    target_calories: int      # 目標卡路里
    target_protein: float     # 目標蛋白質（克）
    target_fat: float        # 目標脂肪（克）

    def __init__(self, target_calories: int = 2000, target_protein: float = 0.0, target_fat: float = 0.0):
        self.target_calories = target_calories
        self.target_protein = target_protein
        self.target_fat = target_fat
