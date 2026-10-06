# AI Usage

## 1. AI Tool Used

**Tool:** ChatGPT

ChatGPT was used as a development assistant during the implementation of this assignment.

---

## 2. How AI Was Used

ChatGPT was used for:

- Understanding the assignment requirements.
- Understanding the HTML structure of the scraping websites.
- Designing the project folder structure.
- Developing the initial scraping logic.
- Implementing automatic pagination.
- Designing the common data model.
- Creating data-cleaning functions.
- Creating validation logic.
- Designing duplicate-detection logic.
- Creating automated test cases.
- Debugging errors during execution.
- Improving project documentation.

---

## 3. Representative Prompts

Some representative prompts used during development were:

1. "Explain this Python web scraping assignment in simple terms."

2. "Create a Python scraper using Requests and BeautifulSoup for Books to Scrape with automatic pagination."

3. "Create a scraper for Quotes to Scrape and handle pagination."

4. "Create reusable cleaning functions for whitespace, price, rating and URL normalization."

5. "Create validation logic for scraped records."

6. "Create a duplicate-detection strategy using normalized text."

7. "Create Pytest test cases for the cleaning, validation and deduplication functions."

8. "Explain the errors from the scraper execution and suggest a reliable fix."

---

## 4. AI-Assisted Parts

AI assistance was used for the initial versions of:

- `scrapers/books_scraper.py`
- `scrapers/quotes_scraper.py`
- `processing/cleaning.py`
- `processing/validation.py`
- `processing/deduplication.py`
- `main.py`
- `tests/test_processing.py`
- `README.md`
- `AI_USAGE.md`

The code was reviewed and tested during development.

---

## 5. Changes Made After Reviewing AI Output

During testing, an additional approach was initially used to fetch category and description information from individual book detail pages.

This resulted in many additional HTTP requests and caused connection and DNS errors during execution.

The approach was reviewed and removed because:

- The fields were not mandatory for every source.
- It created unnecessary traffic.
- The original listing-page scraper was faster and more reliable.
- The assignment allows empty values when a source does not provide a field.

The final implementation uses the listing pages and avoids unnecessary detail-page requests.

---

## 6. Errors and Incorrect Suggestions Discovered

One implementation attempted to request every individual book detail page to obtain additional fields.

During execution, connection-reset and DNS-resolution errors occurred after multiple requests.

The implementation was then changed to use the simpler listing-page approach.

This demonstrated that AI-generated code still needs to be executed, tested and reviewed before being used in the final project.

---

## 7. Testing and Verification

The complete scraping pipeline was executed successfully.

Latest successful execution:

- Books collected: 1000
- Quotes collected: 100
- Total records collected: 1100
- Records after cleaning: 1100
- Rejected records: 0
- Duplicate records removed: 1
- Final records: 1099

Automated tests were also executed using Pytest.

Test result:

```text
6 passed in 0.09s
```

The generated CSV and JSON summary were checked after execution.

---

## 8. Candidate Responsibility

Although AI was used as a coding assistant, the final implementation was reviewed, executed and tested.

The candidate is responsible for understanding the submitted code and can explain:

- How pagination works.
- How data is extracted.
- How cleaning is performed.
- How validation works.
- How duplicates are detected.
- How errors are handled.
- How the final dataset is generated.