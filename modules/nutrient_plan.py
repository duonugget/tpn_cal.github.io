from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NutrientPlan:
    measurement_unit: str #e.g: kcal, g, ml,...
    reference_unit: str #e.g: kg, ibw
    initial_range: Optional[List[float]] = None
    goal_range: Optional[List[float]] = None
    days_to_goal: Optional[int] = None
    daily_intake_range: Optional[List[List[float]]] = None # dành cho các range dinh dưỡng không theo quy luật tăng cố định
    guidelines: Optional[List[str]] = None #e.g: ASPEN 2020, ESPEN 2018
    notes: Optional[str] = None # dành cho các dinh dưỡng ko có định nghĩa range cụ thể mà chỉ lưu ý miệng