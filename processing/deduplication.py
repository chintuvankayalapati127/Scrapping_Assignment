import re


def normalize_for_duplicate(value):
    """Normalize text for duplicate comparison."""

    if value is None:
        return ""

    value = str(value).lower()
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def get_duplicate_key(record):
    """
    Create a key using source and main record content.
    """

    source = normalize_for_duplicate(
        record.get("source")
    )

    title = normalize_for_duplicate(
        record.get("name_or_title")
    )

    author = normalize_for_duplicate(
        record.get("author")
    )

    return (
        source,
        title,
        author
    )


def remove_duplicates(records):
    """Remove duplicate records and return statistics."""

    unique_records = []
    seen = set()
    duplicate_count = 0

    for record in records:
        key = get_duplicate_key(record)

        if key in seen:
            duplicate_count += 1
            continue

        seen.add(key)
        unique_records.append(record)

    return unique_records, duplicate_count