import re
from urllib.parse import urlparse


def clean_text(value):
    """Remove extra whitespace and normalize text."""
    if value is None:
        return ""

    value = str(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean_price(value):
    """Convert price text such as £51.77 into a float."""
    if not value:
        return None

    match = re.search(r"(\d+(?:\.\d+)?)", str(value))

    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None

    return None


def clean_rating(value):
    """Convert book rating words into numbers."""
    ratings = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5
    }

    if not value:
        return None

    value = clean_text(value).lower()

    if value.isdigit():
        number = int(value)
        return number if 1 <= number <= 5 else None

    return ratings.get(value)


def clean_url(value):
    """Return URL only if it looks valid."""
    if not value:
        return ""

    value = str(value).strip()

    parsed = urlparse(value)

    if parsed.scheme in ("http", "https") and parsed.netloc:
        return value

    return ""


def clean_record(record):
    """Clean one scraped record."""

    cleaned = {}

    for key, value in record.items():
        if key not in ("price", "rating"):
            cleaned[key] = clean_text(value)

    cleaned["price"] = clean_price(record.get("price"))
    cleaned["rating"] = clean_rating(record.get("rating"))
    cleaned["source_url"] = clean_url(
        record.get("source_url")
    )

    return cleaned


def clean_records(records):
    """Clean all records."""
    return [clean_record(record) for record in records]