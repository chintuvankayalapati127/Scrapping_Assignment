from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_url
)

from processing.validation import (
    validate_record
)

from processing.deduplication import (
    remove_duplicates
)


def test_clean_text():
    result = clean_text(
        "   Example   Book   "
    )

    assert result == "Example Book"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Three") == 3


def test_clean_url():
    assert clean_url(
        "https://example.com"
    ) == "https://example.com"


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": (
            "https://books.toscrape.com/"
        ),
        "name_or_title": "Example Book",
        "price": 20.50,
        "rating": 4,
        "author": "",
        "tags": "",
        "description": "",
        "category": "",
        "availability": "In stock"
    }

    is_valid, errors = validate_record(
        record
    )

    assert is_valid is True
    assert errors == []


def test_duplicate_removal():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Example Book",
            "author": ""
        },
        {
            "source": "Books to Scrape",
            "name_or_title": " example book ",
            "author": ""
        }
    ]

    unique_records, duplicate_count = (
        remove_duplicates(records)
    )

    assert len(unique_records) == 1
    assert duplicate_count == 1