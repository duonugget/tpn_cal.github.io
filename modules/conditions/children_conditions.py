from conditions import Condition
from dataclasses import dataclass
from ..nutrient_plan import NutrientPlan

@dataclass
class ChildrenCriticalIllness(Condition):
    name: str = "Children (Critically Ill)"
    description: str = (
        "Nutrition management for critically ill children: gradual PN initiation, "
        "individualized energy target, protein progression, glucose limit, and lipid tolerance."
    )
    target = {
        "macro": {
            "energy": {
                "note": NutrientPlan(
                    "kcal",
                    "kg",
                    notes=(
                        "Not full PN for first 2 days; increase over 3–7 days. "
                        "Individualize based on REE (≈1.3×REE in stable phase). "
                        "If refeeding, stop PN for 2 days."
                    ),
                    guidelines="ESPEN/ASPEN Pediatric Critical Care"
                )
            },
            "protein": {
                "replace": NutrientPlan(
                    "g",
                    "kg",
                    goal_range=[1.3, 1.3],
                    notes="Deliver progressively up to 1.3 g/kg protein equivalents per day during critical illness.",
                    guidelines="ESPEN 2020 Pediatric Critical Care"
                )
            },
            "glucose": {
                "replace": NutrientPlan(
                    "mg",
                    "kg/min",
                    goal_range=[0, 5],
                    notes="Do not exceed 5 mg/kg/min glucose infusion rate.",
                    guidelines="ESPEN Pediatric Nutrition"
                )
            },
            "lipid": {
                "replace": NutrientPlan(
                    "g",
                    "kg",
                    goal_range=[0, 1.5],
                    notes=(
                        "Max 1.5 g lipids/kg/day; adapt to individual tolerance. "
                        "EPA+DHA (fish oil) 0.1–0.2 g/kg/day may be provided."
                    ),
                    guidelines="ESPEN Pediatric Nutrition"
                )
            }
        }
    }

