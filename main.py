import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_records
from processing.validation import validate_records
from processing.deduplication import remove_duplicates


# Project directories
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "scraper.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)


def run_pipeline():
    start_time = time.time()

    scraped_at = datetime.now(
        timezone.utc
    ).isoformat()

    logging.info("========== SCRAPING STARTED ==========")

    # --------------------------------------------------
    # 1. SCRAPE
    # --------------------------------------------------

    books = scrape_books()
    quotes = scrape_quotes()

    logging.info(
        f"Books collected: {len(books)}"
    )

    logging.info(
        f"Quotes collected: {len(quotes)}"
    )

    all_records = books + quotes

    collected_counts = {
        "Books to Scrape": len(books),
        "Quotes to Scrape": len(quotes)
    }

    # Add timestamp
    for record in all_records:
        record["scraped_at"] = scraped_at

    # --------------------------------------------------
    # 2. CLEAN
    # --------------------------------------------------

    cleaned_records = clean_records(all_records)

    logging.info(
        f"Records after cleaning: "
        f"{len(cleaned_records)}"
    )

    # --------------------------------------------------
    # 3. VALIDATE
    # --------------------------------------------------

    valid_records, rejected_records = (
        validate_records(cleaned_records)
    )

    logging.info(
        f"Valid records: {len(valid_records)}"
    )

    logging.warning(
        f"Rejected records: "
        f"{len(rejected_records)}"
    )

    # --------------------------------------------------
    # 4. DEDUPLICATE
    # --------------------------------------------------

    unique_records, duplicate_count = (
        remove_duplicates(valid_records)
    )

    logging.info(
        f"Duplicate records removed: "
        f"{duplicate_count}"
    )

    # --------------------------------------------------
    # 5. CREATE DATASET
    # --------------------------------------------------

    columns = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "availability",
        "scraped_at"
    ]

    dataframe = pd.DataFrame(
        unique_records
    )

    # Make sure all expected columns exist
    for column in columns:
        if column not in dataframe.columns:
            dataframe[column] = None

    dataframe = dataframe[columns]

    output_csv = (
        OUTPUT_DIR / "final_dataset.csv"
    )

    dataframe.to_csv(
        output_csv,
        index=False,
        encoding="utf-8"
    )

    # --------------------------------------------------
    # 6. SUMMARY REPORT
    # --------------------------------------------------

    execution_time = round(
        time.time() - start_time,
        2
    )

    summary = {
        "execution_time_seconds": execution_time,
        "records_collected": collected_counts,
        "total_records_collected": len(
            all_records
        ),
        "records_after_cleaning": len(
            cleaned_records
        ),
        "records_rejected": len(
            rejected_records
        ),
        "duplicate_records_removed": (
            duplicate_count
        ),
        "final_record_count": len(
            unique_records
        ),
        "output_file": str(output_csv),
        "completed_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    summary_file = (
        OUTPUT_DIR / "summary_report.json"
    )

    with open(
        summary_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            summary,
            file,
            indent=4
        )

    logging.info(
        f"Final dataset saved to: {output_csv}"
    )

    logging.info(
        f"Summary saved to: {summary_file}"
    )

    logging.info(
        "========== SCRAPING COMPLETED =========="
    )


if __name__ == "__main__":
    run_pipeline()