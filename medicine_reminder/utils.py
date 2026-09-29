from datetime import time, datetime
from .exceptions import ValidationError

def parse_time(text: str) -> time:
    """Parse 'HH:MM' (24h) into a time object."""
    try:
        h, m = text.strip().split(":")
        return time(int(h), int(m))
    except (ValueError, AttributeError) as exc:
        raise ValidationError(f"'{text}' is not a valid HH:MM time.") from exc

def format_dt(dt: datetime) -> str:
    return dt.strftime("%I:%M %p").lstrip("0")
