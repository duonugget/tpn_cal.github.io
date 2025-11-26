from dataclasses import dataclass
from tpn_patient import TpnPatient
from ..nutrient_plan import NutrientPlan
from typing import List, Dict
from ..conditions.children_conditions import ChildrenCriticalIllness
@dataclass
class ChildPatient(TpnPatient):
    age: float
    weight: float

    def __post_init__(self):
        self.conditions = {ChildrenCriticalIllness: self.ask_condition("Children (Critically Ill)")}

    def ask_condition(self, name: str) -> bool:
        answer = input(f"Is the patient {name}? [y/n]: ").strip().lower()
        return answer == "y"

    def get_base_plan(self) -> Dict[str, Dict[str, "NutrientPlan"]]:
        energy = NutrientPlan("kcal", "kg", [90, 120], [90, 120], 0, guidelines=["ESPEN 2018"])
        amino_acids = NutrientPlan(
            "g", "kg",
            [1.5, 2.5] if self.age <= 10 else [0.8, 2],
            [1.5, 2.5] if self.age <= 10 else [0.8, 2],
            0,
            guidelines=["ASPEN 2020"]
        )
        glucose = NutrientPlan(
            "g", "kg",
            [1.5, 2.5] if self.age <= 10 else [2.5, 3],
            [8, 10] if self.age <= 10 else [5, 6],
            0,
            guidelines=["ASPEN 2020"]
        )
        lipids = NutrientPlan(
            "g", "kg",
            [1, 2] if self.age <= 10 else [1, 1],
            [2, 2.5] if self.age <= 10 else [1, 2],
            0,
            guidelines=["ASPEN 2020"]
        )
        fluid = NutrientPlan(
            "mL", "kg",
            [120, 150] if self.age < 1 else
            [80, 120] if self.age <= 2 else
            [80, 100] if self.age <= 5 else
            [60, 80] if self.age <= 12 else
            [50, 70],
            [120, 150] if self.age < 1 else
            [80, 120] if self.age <= 2 else
            [80, 100] if self.age <= 5 else
            [60, 80] if self.age <= 12 else
            [50, 70],
            0,
            guidelines=["ESPEN 2018"]
        )
        sodium = NutrientPlan("mmol", "kg", [2, 3] if self.age < 1 else [1, 3], [2, 3] if self.age < 1 else [1, 3], 0, guidelines=["ESPEN 2018"])
        potassium = NutrientPlan("mmol", "kg", [1, 3], [1, 3], 0, guidelines=["ESPEN 2018"])
        calcium = NutrientPlan("mmol", "kg", [0.5, 0.5] if self.age < 1 else [0.25, 0.4], [0.5, 0.5] if self.age < 1 else [0.25, 0.4], 0, guidelines=["ESPEN 2018"])
        magnesium = NutrientPlan("mmol", "kg", [0.15, 0.15] if self.age < 1 else [0.1, 0.1], [0.15, 0.15] if self.age < 1 else [0.1, 0.1], 0, guidelines=["ESPEN 2018"])
        iron = NutrientPlan("µg", "kg", [50, 100], [50, 100], 0, guidelines=["ESPEN 2018"])
        chloride = NutrientPlan("µg", "kg", [50, 100], [50, 100], 0, guidelines=["ESPEN 2018"])
        phosphorus = NutrientPlan("µg", "kg", [50, 100], [50, 100], 0, guidelines=["ESPEN 2028"])
        acetate = NutrientPlan("mmol", "kg", notes="Use as needed to maintain acid–base balance", guidelines=["ASPEN 2020"])

        zinc = NutrientPlan("µg", "kg", [250, 250] if self.age <= 0.25 else [100, 100] if self.age < 1 else [50, 50],
                            [250, 250] if self.age <= 0.25 else [100, 100] if self.age < 1 else [50, 50],
                            0, guidelines=["ESPEN 2018"])
        copper = NutrientPlan("µg", "kg", [20, 20] if self.weight <= 40 else [200, 500],
                              [20, 20] if self.weight <= 40 else [200, 500], 0, guidelines=["ASPEN 2020"])
        manganese = NutrientPlan("µg", "kg", [1, 1] if self.weight <= 40 else [40, 100],
                                 [1, 1] if self.weight <= 40 else [40, 100], 0, guidelines=["ASPEN 2020"])
        selenium = NutrientPlan("µg", "kg", [2, 2] if self.weight <= 40 else [40, 60],
                                [2, 2] if self.weight <= 40 else [40, 60], 0, guidelines=["ASPEN 2020"])
        chromium = NutrientPlan("µg", "day", [0.2, 0.2] if self.weight <= 40 else [5, 15],
                                [0.2, 0.2] if self.weight <= 40 else [5, 15], 0, guidelines=["ASPEN 2020"])
        iodine = NutrientPlan("µg", "kg", [1, 1], [1, 1], 0, guidelines=["ESPEN 2018"])
        molybdenum = NutrientPlan("µg", "kg", [0.25, 0.25], [0.25, 0.25], 0, guidelines=["ESPEN 2018"])

        vitamins = {
            "vitamin_A": NutrientPlan("µg", "day", [150, 150], [150, 150], 0, guidelines=["ESPEN 2018"]),
            "vitamin_D": NutrientPlan("IU", "day", [400, 600], [400, 600], 0, guidelines=["ESPEN 2018"]),
            "vitamin_E": NutrientPlan("mg", "kg", [11, 11], [11, 11], 0, guidelines=["ESPEN 2018"]),
            "vitamin_K": NutrientPlan("µg", "kg", [200, 200], [200, 200], 0, guidelines=["ESPEN 2018"]),
            "vitamin_C": NutrientPlan("mg", "kg", [80, 80], [80, 80], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B1": NutrientPlan("mg", "kg", [1.2, 1.2], [1.2, 1.2], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B2": NutrientPlan("mg", "kg", [1.4, 1.4], [1.4, 1.4], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B6": NutrientPlan("mg", "kg", [1.0, 1.0], [1.0, 1.0], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B3": NutrientPlan("mg", "kg", [17, 17], [17, 17], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B12": NutrientPlan("µg", "kg", [1, 1], [1, 1], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B5": NutrientPlan("mg", "kg", [5, 5], [5, 5], 0, guidelines=["ESPEN 2018"]),
            "biotin": NutrientPlan("µg", "kg", [20, 20], [20, 20], 0, guidelines=["ESPEN 2018"]),
            "folic_acid": NutrientPlan("mg", "kg", [140, 140], [140, 140], 0, guidelines=["ESPEN 2018"]),
        }

        return {
            "macro": {"energy": energy, "amino_acids": amino_acids, "glucose": glucose, "lipids": lipids, "fluid": fluid},
            "electrolyte": {
                "sodium": sodium, "potassium": potassium, "calcium": calcium, "magnesium": magnesium,
                "phosphorus": phosphorus, "chloride": chloride, "acetate": acetate
            },
            "trace_elements": {
                "zinc": zinc, "copper": copper, "manganese": manganese, "selenium": selenium,
                "chromium": chromium, "iodine": iodine, "molybdenum": molybdenum, "iron": iron
            },
            "vitamins": vitamins,
        }