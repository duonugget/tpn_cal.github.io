from dataclasses import dataclass
from ..conditions.conditions import Condition
from typing import List
@dataclass
class TpnPatient:
    name: str
    age: int # đơn vị của preterm là ngày,term là tháng, đơn vị của children/adult là năm
    height: float
    weight: float
    gender: bool #True = Male
    ibw: float = 0.0
    percentage_ibw: float = 0.0
    bmi: float = 0.0
    conditions: List[Condition] = None

    def __post_init__(self):
        self.ibw = 50 + 2.3 * ((self.height / 2.54) - 60) if self.gender else 45.5 + 2.3 * ((self.height / 2.54) - 60)
        self.bmi = self.weight / ((self.height / 100) ** 2)
        self.percentage_ibw = (self.weight / self.ibw) * 100
