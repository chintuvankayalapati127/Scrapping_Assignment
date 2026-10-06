# Python Web Scraping and Data Processing Pipeline

## 1. Project Overview

This project is a Python-based web scraping and data-processing pipeline.

It collects data from two public scraping practice websites:

- Books to Scrape
- Quotes to Scrape

The collected data is cleaned, validated, checked for duplicates, and combined into one standardized dataset.

The workflow is:

**Scraping → Cleaning → Validation → Deduplication → Consolidation → Output**

---

## 2. Technologies Used

- Python 3.12
- Requests
- BeautifulSoup4
- Pandas
- Pytest

---

## 3. Project Structure

```text
Scrapping_Assignment/
│
├── scrapers/
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── tests/
│   └── test_processing.py
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

---

## 4. Requirements

Python 3.10 or higher is recommended.

The project requires:

- requests
- beautifulsoup4
- pandas
- pytest

---

## 5. Installation

Open the terminal inside the project folder and run:

```bash
python -m pip install -r requirements.txt
```

---

## 6. How to Run

Run the complete scraper using:

```bash
python main.py
```

The program automatically:

1. Scrapes Books to Scrape.
2. Scrapes Quotes to Scrape.
3. Cleans the collected data.
4. Validates the records.
5. Detects and removes duplicates.
6. Creates the final CSV file.
7. Creates the summary JSON file.
8. Saves execution logs.

---

## 7. Data Sources

### Books to Scrape

The scraper collects:

- Book title
- Price
- Rating
- Availability
- Product URL

The scraper automatically follows the next-page link until all available book pages are processed.

### Quotes to Scrape

The scraper collects:

- Quote
- Author
- Tags
- Source URL

The scraper automatically follows the next-page link until all available quote pages are processed.

---

## 8. Data Model

The final dataset uses a common structure:

| Field | Description |
|---|---|
| source | Website from which the record was collected |
| source_url | Original record URL |
| name_or_title | Book title or quote |
| category | Category when available |
| price | Numeric price when available |
| rating | Numeric rating when available |
| author | Author when available |
| tags | Tags when available |
| description | Description when available |
| availability | Availability information for books |
| scraped_at | Time when the record was scraped |

Fields that are not available from a particular website are kept empty. No data is invented.

---

## 9. Data Cleaning

The cleaning process:

- Removes unnecessary whitespace.
- Normalizes text.
- Converts prices such as `£51.77` into numeric values.
- Converts ratings such as `Three` into `3`.
- Checks whether URLs are valid-looking.
- Handles missing values.

The cleaning logic is implemented separately in:

```text
processing/cleaning.py
```

---

## 10. Validation

Records are validated before being added to the final dataset.

Validation checks include:

- Source is recognized.
- Main record value is present.
- Source URL is valid-looking.
- Price is numeric when present.
- Rating is between 1 and 5 when present.

Invalid records are rejected and counted in the summary report.

The validation logic is implemented in:

```text
processing/validation.py
```

---

## 11. Duplicate Detection

Duplicates are detected after cleaning.

The duplicate key uses:

- Source
- Name or title
- Author

Text is normalized before comparison by:

- Converting text to lowercase.
- Removing extra whitespace.
- Removing leading and trailing whitespace.

For example:

```text
Example Book Title
 example book title
EXAMPLE BOOK TITLE
```

can be treated as the same record when the other duplicate-key fields also match.

Duplicate records are removed from the final dataset and the duplicate count is included in the summary report.

The logic is implemented in:

```text
processing/deduplication.py
```

---

## 12. Error Handling and Logging

The scraper handles common problems such as:

- Connection failures
- HTTP errors
- Timeouts
- Missing HTML elements
- Unexpected data formats
- Parsing errors

Errors and warnings are recorded in:

```text
logs/scraper.log
```

A failure on an individual page is handled without unnecessarily crashing the complete program.

---

## 13. Output

The project generates two main output files.

### final_dataset.csv

Contains the cleaned and consolidated records from both websites.

### summary_report.json

Contains information such as:

- Records collected per source
- Total records collected
- Records after cleaning
- Rejected records
- Duplicate records removed
- Final record count
- Execution time

---

## 14. Testing

Automated tests are implemented using Pytest.

Run the tests using:

```bash
python -m pytest
```

The tests cover:

- Text cleaning
- Price conversion
- Rating conversion
- URL validation
- Record validation
- Duplicate removal

Latest test result:

```text
6 passed
```

---

## 15. Assumptions

- The provided websites are publicly accessible.
- The website HTML structure remains compatible with the selectors used.
- Source-specific fields may be empty when they are not available.
- No authentication, CAPTCHA, or access-control mechanism is bypassed.
- The scraper processes pages sequentially.

---

## 16. Known Limitations

- The scraper depends on the current HTML structure of the websites.
- Changes to website layouts may require selector updates.
- The project does not currently use a database.
- Incremental scraping and checkpoint/resume functionality are not implemented.
- Pages are processed sequentially.

---

## 17. AI Usage

ChatGPT was used as a development assistant for:

- Understanding assignment requirements.
- Designing the project structure.
- Developing initial scraping logic.
- Debugging errors.
- Creating cleaning and validation functions.
- Designing duplicate detection.
- Creating automated tests.
- Improving documentation.

Detailed AI usage information is available in:

```text
AI_USAGE.md
```

---

## 18. Verification

The complete pipeline was successfully executed.

Latest successful execution:

- Books collected: **1000**
- Quotes collected: **100**
- Total records collected: **1100**
- Records after cleaning: **1100**
- Rejected records: **0**
- Duplicate records removed: **1**
- Final records: **1099**

Automated testing:

```text
6 passed in 0.09s
```

---

## 19. Future Improvements

Possible future improvements include:

- Retry mechanism with exponential backoff
- Rate limiting
- Parallel or asynchronous scraping
- Incremental scraping
- Checkpoint and resume functionality
- Database integration
- Docker support
- Command-line configuration
- Data-quality reporting