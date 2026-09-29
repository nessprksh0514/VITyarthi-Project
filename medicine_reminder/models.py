from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from .exceptions import ValidationError

FOOD_INSTRUCTIONS = {"before food", "after food", "with food", "any time"}

@dataclass
class Medicine:
    name: str
    dosage: str
    times: list[time]
    duration_days: int
    food_instruction: str
    notes: str = ""
    start_date: date = field(default_factory=date.today)
    taken: set[tuple[date, time]] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValidationError("Medicine name cannot be empty.")
        if not self.times:
            raise ValidationError(f"{self.name}: needs at least one reminder time.")
        if self.duration_days <= 0:
            raise ValidationError(f"{self.name}: duration must be a positive number of days.")
        if self.food_instruction not in FOOD_INSTRUCTIONS:
            raise ValidationError(f"{self.name}: food_instruction must be one of {sorted(FOOD_INSTRUCTIONS)}.")

    @property
    def end_date(self) -> date:
        return self.start_date + timedelta(days=self.duration_days - 1)

    def active_on(self, day: date) -> bool:
        return self.start_date <= day <= self.end_date

    def slots_on(self, day: date) -> list[datetime]:
        return [datetime.combine(day, t) for t in self.times] if self.active_on(day) else []

    def is_taken(self, dt: datetime) -> bool:
        return (dt.date(), dt.time()) in self.taken

    def mark_taken(self, dt: datetime) -> None:
        self.taken.add((dt.date(), dt.time()))
