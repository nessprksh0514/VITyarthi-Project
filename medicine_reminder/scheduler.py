from datetime import date, datetime, timedelta
from difflib import get_close_matches
from typing import Optional
from .models import Medicine
from .exceptions import ValidationError

class ReminderScheduler:
    """Owns the medicine list and implements scheduling modules."""

    def __init__(self, overlap_buffer_minutes: int = 30) -> None:
        self.medicines: dict[str, Medicine] = {}
        self.overlap_buffer = timedelta(minutes=overlap_buffer_minutes)
        self.interactions: dict[frozenset[str], str] = {}

    def add_medicine(self, med: Medicine) -> None:
        key = med.name.strip().lower()
        if key in self.medicines:
            raise ValidationError(f"'{med.name}' is already scheduled.")
        self.medicines[key] = med

    def remove_medicine(self, name: str) -> None:
        key = name.strip().lower()
        if key not in self.medicines:
            raise ValidationError(f"No medicine named '{name}' found.")
        del self.medicines[key]

    def find(self, name: str) -> Optional[Medicine]:
        return self.medicines.get(name.strip().lower())

    def search(self, query: str) -> list[Medicine]:
        matches = get_close_matches(query.strip().lower(), list(self.medicines), n=5, cutoff=0.5)
        return [self.medicines[n] for n in matches]

    def upcoming(self, now: datetime, within: timedelta = timedelta(hours=24)) -> list[tuple[datetime, Medicine]]:
        out = [
            (dt, med)
            for day in (now.date(), now.date() + timedelta(days=1))
            for med in self.medicines.values()
            for dt in med.slots_on(day)
            if now <= dt <= now + within
        ]
        out.sort(key=lambda pair: pair[0])
        return out

    def missed(self, now: datetime, grace: timedelta = timedelta(minutes=30)) -> list[tuple[datetime, Medicine]]:
        out: list[tuple[datetime, Medicine]] = []
        for med in self.medicines.values():
            day, last_day = med.start_date, min(med.end_date, now.date())
            while day <= last_day:
                out += [
                    (dt, med) for dt in med.slots_on(day) if dt + grace < now and not med.is_taken(dt)
                ]
                day += timedelta(days=1)
        out.sort(key=lambda pair: pair[0])
        return out

    def mark_taken(self, name: str, dt: datetime) -> None:
        med = self.find(name)
        if med is None:
            raise ValidationError(f"No medicine named '{name}' found.")
        med.mark_taken(dt)

    def detect_overlaps(self, day: Optional[date] = None) -> list[tuple[Medicine, Medicine, datetime, datetime]]:
        day = day or date.today()
        slots = [(med, dt) for med in self.medicines.values() for dt in med.slots_on(day)]
        return [
            (med_a, med_b, dt_a, dt_b)
            for i, (med_a, dt_a) in enumerate(slots)
            for med_b, dt_b in slots[i + 1 :]
            if med_a is not med_b and abs(dt_a - dt_b) <= self.overlap_buffer
        ]

    def add_interaction(self, name_a: str, name_b: str, note: str) -> None:
        if self.find(name_a) is None or self.find(name_b) is None:
            raise ValidationError("Both medicines must already be scheduled.")
        if not note.strip():
            raise ValidationError("An interaction note is required.")
        self.interactions[frozenset({name_a.strip().lower(), name_b.strip().lower()})] = note.strip()

    def check_interactions(self, day: Optional[date] = None) -> list[tuple[Medicine, Medicine, str]]:
        day = day or date.today()
        active = [m for m in self.medicines.values() if m.active_on(day)]
        return [
            (med_a, med_b, self.interactions[key])
            for i, med_a in enumerate(active)
            for med_b in active[i + 1 :]
            if (key := frozenset({med_a.name.lower(), med_b.name.lower()})) in self.interactions
        ]
