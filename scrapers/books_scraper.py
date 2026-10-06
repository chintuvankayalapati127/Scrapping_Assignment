import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ScrapingAssignment/1.0)"
}


def scrape_books():
    """Scrape books from all available pages."""

    books = []
    next_url = BASE_URL

    while next_url:

        try:
            logging.info(
                f"Scraping books page: {next_url}"
            )

            response = requests.get(
                next_url,
                headers=HEADERS,
                timeout=15
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            book_items = soup.select(
                "article.product_pod"
            )

            for item in book_items:

                try:
                    title_element = item.select_one(
                        "h3 a"
                    )

                    price_element = item.select_one(
                        ".price_color"
                    )

                    availability_element = (
                        item.select_one(
                            ".availability"
                        )
                    )

                    rating_element = item.select_one(
                        "p.star-rating"
                    )

                    title = (
                        title_element.get(
                            "title", ""
                        ).strip()
                        if title_element
                        else ""
                    )

                    price = (
                        price_element.get_text(
                            strip=True
                        )
                        if price_element
                        else ""
                    )

                    availability = (
                        availability_element.get_text(
                            " ",
                            strip=True
                        )
                        if availability_element
                        else ""
                    )

                    rating_classes = (
                        rating_element.get(
                            "class", []
                        )
                        if rating_element
                        else []
                    )

                    rating = next(
                        (
                            value
                            for value in rating_classes
                            if value != "star-rating"
                        ),
                        ""
                    )

                    book_url = (
                        urljoin(
                            next_url,
                            title_element.get("href")
                        )
                        if title_element
                        else ""
                    )

                    books.append({
                        "source": "Books to Scrape",
                        "source_url": book_url,
                        "name_or_title": title,
                        "category": "",
                        "price": price,
                        "rating": rating,
                        "author": "",
                        "tags": "",
                        "description": "",
                        "availability": availability
                    })

                except Exception as error:
                    logging.warning(
                        f"Failed to parse a book: {error}"
                    )

            next_button = soup.select_one(
                "li.next a"
            )

            if next_button:

                next_url = urljoin(
                    next_url,
                    next_button.get("href")
                )

            else:
                next_url = None

        except requests.RequestException as error:

            logging.error(
                f"Failed to fetch {next_url}: {error}"
            )

            break

        except Exception as error:

            logging.error(
                f"Unexpected error on {next_url}: {error}"
            )

            break

    logging.info(
        f"Books scraped successfully: {len(books)}"
    )

    return books