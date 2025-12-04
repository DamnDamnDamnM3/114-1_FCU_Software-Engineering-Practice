"""
NutritionInfo 類別
營養資訊
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class NutritionInfo:
    """營養資訊"""
    calories: int     # 卡路里
    protein: float    # 蛋白質（克）
    carbs: float      # 碳水化合物（克）
    fat: float        # 脂肪（克）

    def __init__(self, calories: int = 0, protein: float = 0.0, carbs: float = 0.0, fat: float = 0.0):
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
