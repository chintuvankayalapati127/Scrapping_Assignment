import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ScrapingAssignment/1.0)"
}


def scrape_quotes():
    """Scrape all quotes from Quotes to Scrape."""

    quotes = []
    next_url = BASE_URL

    while next_url:
        try:
            logging.info(f"Scraping quotes page: {next_url}")

            response = requests.get(
                next_url,
                headers=HEADERS,
                timeout=15
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            quote_items = soup.select("div.quote")

            for item in quote_items:
                try:
                    quote_element = item.select_one(
                        "span.text"
                    )
                    author_element = item.select_one(
                        "small.author"
                    )
                    tag_elements = item.select(
                        "div.tags a.tag"
                    )

                    quote_text = (
                        quote_element.get_text(
                            strip=True
                        )
                        if quote_element
                        else ""
                    )

                    author = (
                        author_element.get_text(
                            strip=True
                        )
                        if author_element
                        else ""
                    )

                    tags = ", ".join(
                        tag.get_text(strip=True)
                        for tag in tag_elements
                    )

                    quotes.append({
                        "source": "Quotes to Scrape",
                        "source_url": next_url,
                        "name_or_title": quote_text,
                        "category": "",
                        "price": "",
                        "rating": "",
                        "author": author,
                        "tags": tags,
                        "description": ""
                    })

                except Exception as error:
                    logging.warning(
                        f"Failed to parse a quote: {error}"
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
        f"Quotes scraped successfully: {len(quotes)}"
    )

    return quotes