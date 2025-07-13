from uuid import UUID

def ensure_uuid(val: str | UUID | None) -> UUID | None:
    """Ensure that the input is a UUID or None."""
    if val is None:
        return None
    if isinstance(val, UUID):
        return val
    return UUID(val)
