from dataclasses import dataclass
from tpn_patient import TpnPatient
from ..nutrient_plan import NutrientPlan
from typing import List, Dict

dataclass
class PretermInfantPatient(TpnPatient):
    def get_base_plan(self) -> Dict[str, Dict[str, NutrientPlan]]:
        energy = NutrientPlan(
            "kcal", "kg", [45, 60], [80, 90], 4,
            guidelines=["NICE 2020"],
            notes="Non-protein energy: 35–45 (D1), 65 target; non-nitrogen ratio 20–30 kcal/g amino acid"
        )
        amino_acids = NutrientPlan(
            "g", "kg", [1.5, 2], [3, 4], 4,
            guidelines=["NICE 2020"]
        ) if self.age <= 4 else NutrientPlan(
            "g", "kg", [3, 4], [3, 4], 0,
            guidelines=["NICE 2020"]
        )
        glucose = NutrientPlan(
            "g", "kg", [6, 9], [9, 16], 4,
            guidelines=["NICE 2020"]
        ) if self.age <= 4 else NutrientPlan(
            "g", "kg", [9, 16], [9, 16], 0,
            guidelines=["NICE 2020"]
        )
        lipids = NutrientPlan(
            "g", "kg", [1, 2], [3, 4], 4,
            guidelines=["NICE 2020"]
        ) if self.age <= 4 else NutrientPlan(
            "g", "kg", [3, 4], [3, 4], 0,
            guidelines=["NICE 2020"]
        )

        if self.weight > 1.5:
            fluid = NutrientPlan("mL", "kg",
                daily_intake_range=[[60, 80], [80, 100], [100, 120], [120, 140], [140, 160]],
                guidelines=["ESPEN 2018"])
            sodium = NutrientPlan("mmol", "kg",
                daily_intake_range=[[0, 3], [0, 3], [0, 3], [2, 5]],
                guidelines=["ESPEN 2018"])
        elif self.weight < 1.0:
            fluid = NutrientPlan("mL", "kg",
                daily_intake_range=[[80, 100], [100, 120], [120, 140], [140, 160], [160, 180]],
                guidelines=["ESPEN 2018"])
            sodium = NutrientPlan("mmol", "kg",
                daily_intake_range=[[0, 3], [0, 3], [0, 5], [2, 7]],
                guidelines=["ESPEN 2018"])
        else:
            fluid = NutrientPlan("mL", "kg",
                daily_intake_range=[[70, 90], [90, 110], [110, 130], [130, 150], [160, 180]],
                guidelines=["ESPEN 2018"])
            sodium = NutrientPlan("mmol", "kg",
                daily_intake_range=[[0, 3], [0, 3], [0, 5], [2, 7]],
                guidelines=["ESPEN 2018"])

        potassium = NutrientPlan("mmol", "kg",
            daily_intake_range=[[0, 3], [2, 3]],
            guidelines=["ESPEN 2018"]
        )
        calcium = NutrientPlan(
            "mmol", "kg", [0.8, 1], [1.5, 2], 2,
            guidelines=["NICE 2020"]
        )
        phosphorus = NutrientPlan(
            "mmol", "kg", [1, 1], [2, 2], 2,
            guidelines=["NICE 2020"]
        )
        iron = NutrientPlan(
            "µg", "kg",
            [0, 0], [225, 250], 28 - self.age if self.age < 28 else 0,
            guidelines=["ESPEN 2018", "NICE 2020"]
        )
        chloride = NutrientPlan(
            "mmol", "kg", [0, 3], [2, 3], 4,
            guidelines=["ESPEN 2018"]
        )
        acetate = NutrientPlan(
            "mmol", "kg",
            notes="Use as needed to maintain acid-base balance",
            guidelines=["ASPEN 2020"]
        )

        zinc = NutrientPlan("µg", "kg", [400, 400], [500, 500], 0, guidelines=["ESPEN 2018"])
        copper = NutrientPlan("µg", "kg", [40, 40], [40, 40], 0, guidelines=["ESPEN 2018"])
        manganese = NutrientPlan("µg", "kg", [1, 1], [1, 1], 0, guidelines=["ASPEN 2020"])
        selenium = NutrientPlan("µg", "kg", [2, 2], [2, 2], 0, guidelines=["ASPEN 2020"])
        chromium = NutrientPlan("µg", "day", [0.05, 0.3], [0.05, 0.3], 0, guidelines=["ASPEN 2020"])
        iodine = NutrientPlan("µg", "kg", [1, 1], [1, 1], 0, guidelines=["ESPEN 2018"])

        return {
            "macro": {
                "energy": energy,
                "amino_acids": amino_acids,
                "glucose": glucose,
                "lipids": lipids,
                "fluid": fluid,
            },
            "electrolyte": {
                "sodium": sodium,
                "potassium": potassium,
                "calcium": calcium,
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
                "iron": iron,
            },
        }