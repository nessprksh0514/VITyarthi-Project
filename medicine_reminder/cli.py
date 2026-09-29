from datetime import date, datetime
from .models import Medicine, FOOD_INSTRUCTIONS
from .scheduler import ReminderScheduler
from .utils import parse_time, format_dt
from .exceptions import ValidationError

DISCLAIMER = (
    "Not a medical diagnosis system -- does not replace professional "
    "medical advice. Interaction warnings below come only from entries "
    "you add yourself; verify them with a doctor or pharmacist."
)

def _prompt(msg: str) -> str:
    return input(msg).strip()

def cmd_add(sched: ReminderScheduler) -> None:
    try:
        name = _prompt("Medicine name: ")
        dosage = _prompt("Dosage schedule (e.g. '1 tablet twice daily'): ")
        raw_times = _prompt("Reminder times, comma-separated HH:MM (e.g. 08:00,20:00): ")
        times = [parse_time(t) for t in raw_times.split(",") if t.strip()]
        duration = int(_prompt("Duration in days: "))
        food = _prompt(f"Food instruction {sorted(FOOD_INSTRUCTIONS)}: ").lower()
        notes = _prompt("Notes (optional): ")
        sched.add_medicine(Medicine(name, dosage, times, duration, food, notes))
        print(f"Added {name}.")
    except (ValidationError, ValueError) as exc:
        print(f"Could not add medicine: {exc}")

def cmd_remove(sched: ReminderScheduler) -> None:
    try:
        sched.remove_medicine(_prompt("Medicine name to remove: "))
        print("Removed.")
    except ValidationError as exc:
        print(exc)

def cmd_search(sched: ReminderScheduler) -> None:
    hits = sched.search(_prompt("Search for medicine: "))
    if not hits:
        print("No matches.")
        return
    for med in hits:
        print(f"- {med.name} ({med.dosage}), {med.food_instruction}")

def cmd_list(sched: ReminderScheduler) -> None:
    if not sched.medicines:
        print("No medicines scheduled.")
        return
    for med in sched.medicines.values():
        times = ", ".join(t.strftime("%H:%M") for t in med.times)
        print(f"- {med.name}: {med.dosage} at {times}, {med.duration_days}d, {med.food_instruction}")

def cmd_upcoming(sched: ReminderScheduler) -> None:
    rows = sched.upcoming(datetime.now())
    if not rows:
        print("No upcoming reminders in the next 24 hours.")
        return
    print("Upcoming:")
    for dt, med in rows:
        print(f"{dt.strftime('%Y-%m-%d')} {format_dt(dt)} - {med.name}")

def cmd_missed(sched: ReminderScheduler) -> None:
    rows = sched.missed(datetime.now())
    if not rows:
        print("No missed doses.")
        return
    print("Missed doses:")
    for dt, med in rows:
        print(f"{dt.strftime('%Y-%m-%d')} {format_dt(dt)} - {med.name}")

def cmd_check(sched: ReminderScheduler) -> None:
    overlaps = sched.detect_overlaps()
    interactions = sched.check_interactions()
    if not overlaps and not interactions:
        print("No schedule conflicts or recorded interactions today.")
        return
    for med_a, med_b, dt_a, dt_b in overlaps:
        print(
            f"Overlap: {med_a.name} ({format_dt(dt_a)}) and {med_b.name} ({format_dt(dt_b)}) "
            "are close together."
        )
    if interactions:
        print("\nWarning:")
        print("These medicines have a recorded interaction note.")
        for med_a, med_b, note in interactions:
            print(f"{med_a.name} + {med_b.name}: {note}")
        print("Consult a qualified doctor or pharmacist.")

def cmd_taken(sched: ReminderScheduler) -> None:
    try:
        name = _prompt("Medicine name: ")
        med = sched.find(name)
        if not med:
            raise ValidationError(f"No medicine named '{name}' found.")
            
        raw = _prompt("Dose time to mark (HH:MM for today, YYYY-MM-DD HH:MM for past, blank = oldest missed): ")
        
        if not raw:
            now = datetime.now()
            missed_doses = [dt for dt, m in sched.missed(now) if m is med]
            if missed_doses:
                dt = missed_doses[0] 
            else:
                slots = med.slots_on(now.date())
                if not slots:
                    raise ValidationError("No doses scheduled for today.")
                dt = min(slots, key=lambda s: abs(s - now))
        else:
            parts = raw.split()
            if len(parts) == 1:
                dt = datetime.combine(date.today(), parse_time(parts[0]))
            elif len(parts) == 2:
                try:
                    d = datetime.strptime(parts[0], "%Y-%m-%d").date()
                    dt = datetime.combine(d, parse_time(parts[1]))
                except ValueError:
                    raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
            else:
                raise ValidationError("Invalid input format.")
                
        sched.mark_taken(name, dt)
        print(f"Marked {dt.strftime('%Y-%m-%d')} {format_dt(dt)} dose as taken.")
    except (ValidationError, ValueError) as exc:
        print(f"Could not record dose: {exc}")

def cmd_interaction(sched: ReminderScheduler) -> None:
    try:
        a = _prompt("First medicine name: ")
        b = _prompt("Second medicine name: ")
        note = _prompt("Interaction note (from a doctor/pharmacist/verified source): ")
        sched.add_interaction(a, b, note)
        print("Interaction note saved.")
    except ValidationError as exc:
        print(exc)

MENU = {
    "1": ("Add medicine", cmd_add),
    "2": ("Remove medicine", cmd_remove),
    "3": ("Search medicines", cmd_search),
    "4": ("List all medicines", cmd_list),
    "5": ("Show upcoming reminders", cmd_upcoming),
    "6": ("Show missed doses", cmd_missed),
    "7": ("Check overlaps & interactions", cmd_check),
    "8": ("Mark a dose as taken", cmd_taken),
    "9": ("Add an interaction note", cmd_interaction),
}

def main() -> None:
    sched = ReminderScheduler()
    print("Medicine Reminder and Interaction Safety Checker")
    print(DISCLAIMER)
    while True:
        print("\n" + "\n".join(f"{k}. {label}" for k, (label, _fn) in MENU.items()) + "\n0. Exit")
        choice = _prompt("> ")
        if choice == "0":
            print("Goodbye.")
            return
        action = MENU.get(choice)
        if action is None:
            print("Invalid choice.")
            continue
        action[1](sched)
