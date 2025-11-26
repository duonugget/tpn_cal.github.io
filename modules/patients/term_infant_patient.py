from dataclasses import dataclass
from tpn_patient import TpnPatient
from ..nutrient_plan import NutrientPlan
from typing import List, Dict

@dataclass
class TermInfantPatient(TpnPatient):
    def get_base_plan(self) -> Dict[str, Dict[str, NutrientPlan]]:
        energy = NutrientPlan(
            "kcal", "kg", [45, 60], [80, 90], 4,
            guidelines=["NICE 2020"],
            notes="Non-protein energy 35–45 (D1), 65 target; non-nitrogen ratio 20–30 kcal/g amino acid"
        )
        amino_acids = NutrientPlan(
            "g", "kg", [2.5, 3], [2.5, 3], 0,
            guidelines=["ASPEN 2020"]
        )
        glucose = NutrientPlan(
            "g", "kg", [6, 8], [10, 14], 4,
            guidelines=["ASPEN 2020"]
        )
        lipids = NutrientPlan(
            "g", "kg", [0.5, 1], [2.5, 3], 4,
            guidelines=["ASPEN 2020"]
        )
        ratio = NutrientPlan(
            "kcal", "g",
            notes="Provide 60–75% carbohydrate, 25–40% lipid; maintain non-nitrogen ratio 20–30 kcal/g amino acid (23–34 kcal total)",
            guidelines=["NICE 2020"]
        )
        fluid = NutrientPlan(
            "mL", "kg",
            daily_intake_range=[[40, 60], [50, 70], [60, 80], [60, 100], [100, 140]],
            guidelines=["ESPEN 2018"]
        )
        sodium = NutrientPlan(
            "mmol", "kg",
            daily_intake_range=[[0, 2], [0, 2], [0, 2], [1, 3], [1, 3]],
            guidelines=["ESPEN 2018"]
        )
        potassium = NutrientPlan(
            "mmol", "kg",
            daily_intake_range=[[0, 2], [0, 2], [0, 2], [1, 3], [1, 3]],
            guidelines=["ESPEN 2018"]
        )
        calcium = NutrientPlan(
            "mmol", "kg", [0.5, 4], [0.5, 4], 0,
            guidelines=["ASPEN 2020"]
        )
        magnesium = NutrientPlan(
            "mmol", "kg",
            [0.1, 0.2] if self.age <= 6 else [0.15, 0.15],
            [0.1, 0.2] if self.age <= 6 else [0.15, 0.15],
            0,
            guidelines=["ESPEN 2018"]
        )
        iron = NutrientPlan(
            "mg", "kg",
            [0, 0] if self.age < 28 else [0.5, 4],
            [0, 0] if self.age < 28 else [0.5, 4],
            0,
            guidelines=["ESPEN 2018", "NICE 2020"]
        )
        chloride = NutrientPlan(
            "mmol", "kg",
            daily_intake_range=[[0, 3], [0, 3], [0, 3], [2, 3], [2, 3], [2, 3], [2, 3]],
            guidelines=["ESPEN 2018"]
        )
        phosphorus = NutrientPlan(
            "mmol", "kg",
            [0.7, 1.3] if self.age <= 6 else [0.5, 0.5],
            [0.7, 1.3] if self.age <= 6 else [0.5, 0.5],
            0,
            guidelines=["ESPEN 2028"]
        )
        acetate = NutrientPlan(
            "mmol", "kg",
            notes="Use as needed to maintain acid–base balance",
            guidelines=["ASPEN 2020"]
        )

        zinc = NutrientPlan(
            "µg", "kg",
            [250, 250] if self.age <= 3 else [100, 100],
            [250, 250] if self.age <= 3 else [100, 100],
            0,
            guidelines=["ESPEN 2018"]
        )
        copper = NutrientPlan("µg", "kg", [20, 20], [20, 20], 0, guidelines=["ESPEN 2018"])
        manganese = NutrientPlan("µg", "kg", [1, 1], [1, 1], 0, guidelines=["ASPEN 2020"])
        selenium = NutrientPlan("µg", "kg", [2, 3], [2, 3], 0, guidelines=["ESPEN 2018"])
        chromium = NutrientPlan("µg", "day", [0.2, 0.2], [0.2, 0.2], 0, guidelines=["ASPEN 2020"])
        iodine = NutrientPlan("µg", "kg", [1, 1], [1, 1], 0, guidelines=["ESPEN 2018"])
        molybdenum = NutrientPlan("µg", "kg", [0.25, 0.25], [0.25, 0.25], 0, guidelines=["ESPEN 2018"])

        vitamins = {
            "vitamin_A": NutrientPlan("IU", "kg", [150, 300], [150, 300], 0, guidelines=["ESPEN 2018"]),
            "vitamin_D": NutrientPlan("IU", "kg", [40, 150], [40, 150], 0, guidelines=["ESPEN 2018"]),
            "vitamin_E": NutrientPlan("mg", "kg", [2.8, 3.5], [2.8, 3.5], 0, guidelines=["ESPEN 2018"]),
            "vitamin_K": NutrientPlan("µg", "kg", [10, 10], [10, 10], 0, guidelines=["ESPEN 2018"]),
            "vitamin_C": NutrientPlan("mg", "kg", [15, 25], [15, 25], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B1": NutrientPlan("mg", "kg", [0.35, 0.5], [0.35, 0.5], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B2": NutrientPlan("mg", "kg", [0.15, 0.2], [0.15, 0.2], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B6": NutrientPlan("mg", "kg", [0.15, 0.2], [0.15, 0.2], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B3": NutrientPlan("mg", "kg", [4, 6.8], [4, 6.8], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B12": NutrientPlan("µg", "kg", [0.3, 0.3], [0.3, 0.3], 0, guidelines=["ESPEN 2018"]),
            "vitamin_B5": NutrientPlan("mg", "kg", [2.5, 2.5], [2.5, 2.5], 0, guidelines=["ESPEN 2018"]),
            "biotin": NutrientPlan("µg", "kg", [5, 8], [5, 8], 0, guidelines=["ESPEN 2018"]),
            "folic_acid": NutrientPlan("mg", "kg", [56, 56], [56, 56], 0, guidelines=["ESPEN 2018"]),
        }

        return {
            "macro": {
                "energy": energy,
                "amino_acids": amino_acids,
                "glucose": glucose,
                "lipids": lipids,
                "ratio": ratio,
                "fluid": fluid,
            },
            "electrolyte": {
                "sodium": sodium,
                "potassium": potassium,
                "calcium": calcium,
                "magnesium": magnesium,
                "phosphorus": phosphorus,
                "chloride": chloride,
                "acetate": acetate,
            },
            "trace_elements": {
                "zinc": zinc,
                "copper": copper,
                "manganese": manganese,
                "selenium": selenium,
                "chromium": chromium,
                "iodine": iodine,
                "molybdenum": molybdenum,
                "iron": iron,
            },
            "vitamins": vitamins,
        }