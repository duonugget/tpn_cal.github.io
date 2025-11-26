from dataclasses import dataclass
from typing import Dict, Type
from modules.patients.tpn_patient import TpnPatient
from modules.conditions.conditions import Condition
from modules.conditions.adult_conditions import *
from modules.nutrient_plan import NutrientPlan


@dataclass
class AdultPatient(TpnPatient):
    conditions: Dict[Type["Condition"], bool]

    def __init__(self, name: str, age: int, height: float, weight: float, gender: bool, conditions: Dict = None):
        super().__init__(
            name=name,
            age=age,
            height=height,
            weight=weight,
            gender=gender,
            conditions=conditions or {}
        )
        self.conditions = conditions or {}

    def get_base_plan(self) -> Dict[str, Dict[str, NutrientPlan]]:
        return {
            "macro": {
                "protein_amino_acids": NutrientPlan("g", "kg", [0.8, 1.5], [0.8, 1.5], 0, ["ASPEN 2020"],notes="Additional 15–30 g/L exudate"),
                "energy": NutrientPlan("kcal", "kg", [20, 30], [20, 30], 0, ["ASPEN 2020"]),
                "dextrose": NutrientPlan("mg", "kg/min", [4, 5], [4, 5], 0, ["ASPEN 2020"]),
                "lipid_emulsion": NutrientPlan("g", "kg", [1, 1], [1, 1], 0, ["ASPEN 2020"]),
                "fluid": NutrientPlan("mL", "kg", [30, 40], [30, 40], 0, ["ASPEN 2020"]),
            },
            "electrolyte": {
                "calcium": NutrientPlan("mEq", "day", [10, 15], [10, 15], 0, ["ASPEN 2020"]),
                "magnesium": NutrientPlan("mEq", "day", [8, 20], [8, 20], 0, ["ASPEN 2020"]),
                "phosphorus": NutrientPlan("mmol", "day", [20, 40], [20, 40], 0, ["ASPEN 2020"]),
                "sodium": NutrientPlan("mEq", "kg", [1, 2], [1, 2], 0, ["ASPEN 2020"]),
                "potassium": NutrientPlan("mEq", "kg", [1, 2], [1, 2], 0, ["ASPEN 2020"]),
                "acetate": NutrientPlan("mEq", "kg", None, None, 0, ["ASPEN 2020"]),
                "chloride": NutrientPlan("mEq", "kg", None, None, 0, ["ASPEN 2020"]),
            },
            "vitamins": {
                "thiamine_B1": NutrientPlan("mg", "day", [6, 6], [6, 6], 0, ["ASPEN 2020"]),
                "riboflavin_B2": NutrientPlan("mg", "day", [3.6, 3.6], [3.6, 3.6], 0, ["ASPEN 2020"]),
                "niacin_B3": NutrientPlan("mg", "day", [40, 40], [40, 40], 0, ["ASPEN 2020"]),
                "folic_acid": NutrientPlan("µg", "day", [600, 600], [600, 600], 0, ["ASPEN 2020"]),
                "pantothenic_acid": NutrientPlan("mg", "day", [15, 15], [15, 15], 0, ["ASPEN 2020"]),
                "pyridoxine_B6": NutrientPlan("mg", "day", [6, 6], [6, 6], 0, ["ASPEN 2020"]),
                "cyanocobalamin_B12": NutrientPlan("µg", "day", [5, 5], [5, 5], 0, ["ASPEN 2020"]),
                "biotin": NutrientPlan("µg", "day", [60, 60], [60, 60], 0, ["ASPEN 2020"]),
                "ascorbic_acid_C": NutrientPlan("mg", "day", [200, 200], [200, 200], 0, ["ASPEN 2020"]),
                "vitamin_A": NutrientPlan("µg", "day", [990, 990], [990, 990], 0, ["ASPEN 2020"]),
                "vitamin_D": NutrientPlan("µg", "day", [5, 5], [5, 5], 0, ["ASPEN 2020"]),
                "vitamin_E": NutrientPlan("mg", "day", [10, 10], [10, 10], 0, ["ASPEN 2020"]),
                "vitamin_K": NutrientPlan("µg", "day", [150, 150], [150, 150], 0, ["ASPEN 2020"]),
            },
            "trace_elements": {
                "chromium": NutrientPlan("µg", "day", [0, 10], [0, 10], 0, ["ASPEN 2020"]),
                "copper": NutrientPlan("mg", "day", [0.3, 0.5], [0.3, 0.5], 0, ["ASPEN 2020"]),
                "manganese": NutrientPlan("µg", "day", [55, 55], [55, 55], 0, ["ASPEN 2020"]),
                "selenium": NutrientPlan("µg", "day", [60, 100], [60, 100], 0, ["ASPEN 2020"]),
                "zinc": NutrientPlan("mg", "day", [3, 5], [3, 5], 0, ["ASPEN 2020"]),
            }
        }
