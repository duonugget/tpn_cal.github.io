from modules.conditions.conditions import Condition
from dataclasses import dataclass
from modules.nutrient_plan import NutrientPlan

@dataclass
class CriticallyIllAdult(Condition):
    name: str = "Critically Ill Adult"
    description: str = "General conditions related to critically ill adult patients."


@dataclass
class ObeseAdult(Condition):
    name: str = "Obese Adult"
    description: str = "Nutritional management for obese adult patients."


@dataclass
class RenalDisease(Condition):
    name: str = "Renal Disease"
    description: str = "Conditions related to acute or chronic kidney diseases."


@dataclass
class HepaticDisease(Condition):
    name: str = "Hepatic Disease"
    description: str = "Conditions related to liver dysfunction or hepatic failure."


@dataclass
class CardiacDisease(Condition):
    name: str = "Cardiac Disease"
    description: str = "Conditions related to cardiac disease and associated metabolic effects."


@dataclass
class TraumaticBrainInjury(CriticallyIllAdult):
    name: str = "Traumatic Brain Injury"
    description: str = "Increased amino acid requirement due to hypermetabolism and catabolism."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[1.2, 2.5], guidelines="ASPEN 2020")
            }
        }
    }

@dataclass
class Burns(CriticallyIllAdult):
    name: str = "Burns"
    description: str = "Higher protein need for wound healing and tissue repair."
    target = {
        "macro": {
            "energy": {
                "replace": NutrientPlan(
                    "kcal",
                    "kg",
                    goal_range=[22, 25],
                    guidelines="ASPEN 2020"
                )
            },
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[1.5, 2.0])
            },
            "lipids": {
                "restrict": 1
            }
        }
    }

class Sepsis(CriticallyIllAdult):
    name: str = "Sepsis"
    description: str = "Higher protein need for wound healing and tissue repair."
    target = {
        "micro": {
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[0, 0])
            }
        }
    }

@dataclass
class OpenAbdomen(CriticallyIllAdult):
    name: str = "Open abdomen"
    description: str = "Additional amino acids due to exudate losses."
    target = {
        "macro": {
            "amino_acids": {
                "add_fixed": NutrientPlan(
                    "g",
                    "kg",
                    notes="Additional 15–30 g/L exudate",
                    guidelines="ASPEN 2020"
                )
            }
        }
    }


@dataclass
class Obese(ObeseAdult):
    name: str = "Obese"
    description: str = "Adjusted macronutrient requirements based on ideal body weight."
    target = {
        "macro": {
            "lipids": {
                "restrict": 1
            }
        }
    }


@dataclass
class AcuteKidneyInjury(RenalDisease):
    name: str = "Acute Kidney Injury"
    description: str = "Adjust amino acid dose based on kidney function."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[0.8, 2.0])
            }
        }
    }

@dataclass
class AcuteKidneyInjury_NoRRT(AcuteKidneyInjury):
    name: str = "Acute Kidney Injury (No RRT)"
    description: str = "For AKI patients not receiving renal replacement therapy."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan(
                    "g",
                    "kg",
                    goal_range=[1.0, 1.3],
                    guidelines="ESPEN 2021"
                )
            }
        }
    }


@dataclass
class AcuteKidneyInjury_IntermittentRRT(AcuteKidneyInjury):
    name: str = "Acute Kidney Injury (Intermittent RRT)"
    description: str = "For AKI patients on intermittent renal replacement therapy."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan(
                    "g",
                    "kg",
                    goal_range=[1.3, 1.5],
                    guidelines="ESPEN 2021"
                )
            }
        }
    }

@dataclass
class AcuteKidneyInjury_CRRT(AcuteKidneyInjury):
    name: str = "Acute Kidney Injury (CRRT)"
    description: str = "For AKI patients receiving continuous renal replacement therapy."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan(
                    "g",
                    "kg",
                    goal_range=[1.5, 1.7],
                    guidelines="ESPEN 2021"
                )
            }
        }
    }


@dataclass
class ChronicKidneyFailure_MaintenanceHD(AcuteKidneyInjury):
    name: str = "Chronic Kidney Failure (Maintenance Hemodialysis)"
    description: str = "Protein adjustment for chronic kidney disease with maintenance hemodialysis."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan(
                    "g",
                    "kg",
                    goal_range=[1.2, 1.2],
                    guidelines="ASPEN 2020"
                )
            }
        }
    }



@dataclass
class ChronicKidneyFailure(RenalDisease):
    name: str = "Chronic Kidney Failure"
    description: str = "Protein adjustment for dialysis patients."
    target = {
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[1.2, 1.2])
            }
        }
    }


@dataclass
class AcuteLiverFailure(HepaticDisease):
    name: str = "Liver Failure"
    description: str = "Adjust amino acid intake based on dry weight and tolerance."
    target = {
        "macro": {
            "energy": {
                "replace": NutrientPlan(
                    "kcal",
                    "kg",
                    goal_range=[30, 35],
                    guidelines="EASL"
                )
            },
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[1.2, 2.0])
            }
        }
    }


@dataclass
class HeartFailure(CardiacDisease):
    name: str = "Heart Disease"
    description: str = "Nutrition plan for patients with cardiac disease."
    target = {
        "energy": {
            "kcal": {
                "replace": NutrientPlan("kcal", "kg", goal_range=[20, 25])
            }
        },
        "macro": {
            "amino_acids": {
                "replace": NutrientPlan("g", "kg", goal_range=[1.0, 1.5])
            },
            "lipids": {
                "restrict": 1
            }
        },
        "electrolyte": {
            "sodium": {"restrict": 0},
            "potassium": {"replace": None},
            "zinc": {"replace": NutrientPlan("mg", "day", goal_range=[2.5, 5])},
            "copper": {"replace": NutrientPlan("mcg", "day", goal_range=[300, 500])},
            "selenium": {"replace": NutrientPlan("mcg", "day", goal_range=[60, 100])},
        }
    }