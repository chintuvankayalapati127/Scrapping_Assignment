from urllib.parse import urlparse


VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape"
}


def is_valid_url(url):
    """Check whether a URL looks valid."""
    if not url:
        return False

    parsed = urlparse(url)

    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.netloc)
    )


def validate_record(record):
    """Validate a cleaned record."""

    errors = []

    if record.get("source") not in VALID_SOURCES:
        errors.append("Invalid source")

    if not record.get("name_or_title"):
        errors.append("Missing name_or_title")

    if not is_valid_url(record.get("source_url")):
        errors.append("Invalid source URL")

    price = record.get("price")

    if price is not None and (
        not isinstance(price, (int, float))
        or price < 0
    ):
        errors.append("Invalid price")

    rating = record.get("rating")

    if rating is not None and rating not in range(1, 6):
        errors.append("Invalid rating")

    return len(errors) == 0, errors


def validate_records(records):
    """Validate all records."""

    valid_records = []
    rejected_records = []

    for record in records:
        is_valid, errors = validate_record(record)

        if is_valid:
            valid_records.append(record)
        else:
            rejected_records.append({
                "record": record,
                "errors": errors
            })

    return valid_records, rejected_records