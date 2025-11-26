from copy import deepcopy
import statistics
import pandas as pd
from typing import List, Optional
from modules.nutrient_plan import NutrientPlan

class TpnPlanner:
    def __init__(self, patient, total_days: int = 7):
        self.patient = patient
        self.total_days = total_days
        self.base_plan = deepcopy(patient.get_base_plan())
        self.final_plan = deepcopy(self.base_plan)
        self.notes: List[str] = []

    def midpoint(self, values: Optional[List[float]]) -> Optional[float]:
        if not values:
            return None
        if len(values) == 1:
            return values[0]
        if all(v is not None for v in values):
            return round(statistics.mean(values), 3)
        return None

    def interpolate(self, start: Optional[float], end: Optional[float], days: int) -> List[Optional[float]]:
        """Linearly interpolate between start and end over number of days."""
        if start is None and end is None:
            return [None] * days
        if days <= 1:
            return [round(end, 3) if end is not None else None]
        if start is None:
            return [round(end, 3)] * days
        if end is None:
            return [round(start, 3)] * days
        step = (end - start) / (days - 1)
        return [round(start + i * step, 3) for i in range(days)]

    def get_reference_value(self) -> float:
        """Return IBW or weight if available, else 1."""
        if hasattr(self.patient, "ibw") and self.patient.ibw:
            return self.patient.ibw
        if hasattr(self.patient, "weight") and self.patient.weight:
            return self.patient.weight
        return 1  # fallback

    def collect_plan_notes(self, plan_dict):
        """Collect notes from a plan."""
        for category, nutrients in plan_dict.items():
            for nutrient_name, plan in nutrients.items():
                if plan.notes:
                    self.notes.append(f"{category} - {nutrient_name}: {plan.notes}")

    def apply_conditions(self):
        """Apply patient conditions to the final plan."""
        for condition_type, active in getattr(self.patient, "conditions", {}).items():
            if not active:
                continue
            condition = condition_type()
            if hasattr(condition, "modify_plan"):
                condition.modify_plan(self.final_plan, self.patient)

    def generate_daily_plan(self) -> pd.DataFrame:
        """Generate a daily TPN plan as a pivoted DataFrame."""
        # Collect notes from base plan

        # Apply all conditions
        self.apply_conditions()
        self.collect_plan_notes(self.final_plan)

        ref_value = self.get_reference_value()
        records = []

        for category, nutrients in self.final_plan.items():
            for nutrient_name, plan in nutrients.items():
                # Compute initial and goal values
                init = self.midpoint(plan.initial_range)
                goal = self.midpoint(plan.goal_range) or init  # fallback if goal_range missing

                daily_values = self.interpolate(init, goal, self.total_days)

                for day, value in enumerate(daily_values, start=1):
                    # Scale only if unit is per kg (example: "g/kg" or "mg/kg")
                    if plan.measurement_unit.lower() in ["g/kg", "mg/kg"]:
                        scaled_value = round(value * ref_value, 3) if value is not None else None
                    else:
                        scaled_value = round(value, 3) if value is not None else None

                    records.append({
                        "Day": day,
                        "Category": category,
                        "Nutrient": nutrient_name,
                        "Value": scaled_value,
                        "Unit": plan.measurement_unit,
                        "Per": plan.measurement_unit
                    })

        df = pd.DataFrame(records)

        # Print notes
        if self.notes:
            print("\n--- Planner Notes ---")
            for note in self.notes:
                print("•", note)

        # Pivot table: Days as columns, Nutrients as rows
        pivoted = df.pivot_table(index=["Category", "Nutrient"], columns="Day", values="Value")
        return pivoted
