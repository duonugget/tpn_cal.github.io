from dataclasses import dataclass
from typing import List, Optional
from typing import Dict
from ..nutrient_plan import NutrientPlan
from dataclasses import dataclass

@dataclass
class Condition:
    name: str
    description: str
    target: Dict[
        str,  # category (e.g: marco, electrolytes, vitamins,...)
        Dict[
            str,  # nutrient name
            Dict[
                str, # phân loại condition (có thể định nghĩa range/NutrientPlan mới hoặc đưa ra giá trị dinh dưỡng giới hạn)
                Optional[float | NutrientPlan]
            ]
        ]
    ] = None
    guidelines: List[str] = None
