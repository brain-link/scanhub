from uuid import UUID
from datetime import date


def ensure_uuid(val: str | UUID | None) -> UUID | None:
    """Ensure that the input is a UUID or None."""
    if val is None:
        return None
    if isinstance(val, UUID):
        return val
    return UUID(val)


def calc_age_from_date(birth_date: date) -> int:
    """Calculate age in years from a given birth date.

    Parameters
    ----------
    birth_date
        Date of birth

    Returns
    -------
        Age in years as int
    """
    today = date.today()
    age = today.year - birth_date.year
    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age
