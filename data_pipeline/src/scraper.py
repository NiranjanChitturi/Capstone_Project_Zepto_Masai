"""
Module 1 - Data Pipeline
------------------------
Web scraping utilities for Books to Scrape.

This module is responsible for:
1. Sending HTTP requests to the source website.
2. Validating the HTTP response.
3. Parsing the returned HTML using BeautifulSoup.

The actual book extraction logic will be added in subsequent steps.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Base URL of the public practice website used for this project.
BASE_URL = "https://books.toscrape.com/"


# ---------------------------------------------------------------------------
# Web Page Fetching
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> BeautifulSoup:
    """
    Fetch a web page and return its parsed HTML document.

    Parameters
    ----------
    url : str
        URL of the web page to retrieve.

    Returns
    -------
    BeautifulSoup
        Parsed HTML document.

    Raises
    ------
    requests.HTTPError
        If the server returns an unsuccessful HTTP status code.
    requests.RequestException
        If a network-related error occurs.
    """

    # Send an HTTP GET request to the specified URL.
    # A timeout prevents the program from waiting indefinitely.
    response = requests.get(url, timeout=15)

    # Raise an exception automatically if the response contains
    # an HTTP error status such as 404 or 500.
    response.raise_for_status()

    # Parse the HTML response using BeautifulSoup.
    # "html.parser" is Python's built-in HTML parser and is
    # sufficient for this project.
    return BeautifulSoup(response.text, "html.parser")

# ---------------------------------------------------------------------------
# Book Extraction
# ---------------------------------------------------------------------------

def extract_book(product: BeautifulSoup) -> dict:
    """
    Extract the required book information from a product card.

    Parameters
    ----------
    product : BeautifulSoup
        BeautifulSoup element representing one book's
        <article class="product_pod"> element.

    Returns
    -------
    dict
        Dictionary containing the raw book information:
        title, price, star_rating, availability, and category.

    Notes
    -----
    The category is not available directly inside the product card.
    It will be determined from the category/page context when we build
    the multi-page scraper.
    """

    # Extract the full book title from the HTML title attribute.
    title_element = product.select_one("h3 a")
    title = title_element.get("title", "").strip()

    # Extract the price text.
    price_element = product.select_one("p.price_color")
    price = price_element.get_text(strip=True)

    # Extract the textual star rating.
    # Example: <p class="star-rating Three">
    rating_element = product.select_one("p.star-rating")
    rating_classes = rating_element.get("class", []) if rating_element else []

    # The rating is the class other than "star-rating".
    star_rating = next(
        (
            class_name
            for class_name in rating_classes
            if class_name != "star-rating"
        ),
        "",
    )

    # Extract the availability text.
    availability_element = product.select_one("p.availability")
    availability = (
        availability_element.get_text(" ", strip=True)
        if availability_element
        else ""
    )

    return {
        "title": title,
        "price": price,
        "star_rating": star_rating,
        "availability": availability,
        "category": None,
    }

# ---------------------------------------------------------------------------
# Category Discovery
# ---------------------------------------------------------------------------

def get_category_urls(
    soup: BeautifulSoup,
    selected_categories: list[str],
) -> dict[str, str]:
    """
    Discover URLs for the requested book categories.

    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML of the Books to Scrape home page.

    selected_categories : list[str]
        Category names that should be included in the scrape.

    Returns
    -------
    dict[str, str]
        Mapping of category name to its relative URL.

    Raises
    ------
    ValueError
        If one or more requested categories cannot be found.
    """

    # Find all category links displayed in the site's navigation menu.
    category_links = soup.select("ul.nav-list ul li a")

    # Build a lookup dictionary:
    # {
    #     "Mystery": "catalogue/category/books/mystery_3/index.html",
    #     ...
    # }
    available_categories = {
        link.get_text(strip=True): link.get("href")
        for link in category_links
    }

    # Identify any requested categories that are not available.
    missing_categories = [
        category
        for category in selected_categories
        if category not in available_categories
    ]

    # Fail early rather than silently scraping the wrong categories.
    if missing_categories:
        raise ValueError(
            f"Category/categories not found: {missing_categories}"
        )

    # Return only the categories requested by the pipeline.
    return {
        category: available_categories[category]
        for category in selected_categories
    }


# ---------------------------------------------------------------------------
# URL Construction
# ---------------------------------------------------------------------------

def build_absolute_url(base_url: str, relative_url: str) -> str:
    """
    Convert a relative website URL into an absolute URL.

    Parameters
    ----------
    base_url : str
        Base URL of the website.

    relative_url : str
        Relative URL returned by the website.

    Returns
    -------
    str
        Fully qualified URL.
    """

    return urljoin(base_url, relative_url)

# ---------------------------------------------------------------------------
# Pagination Handling
# ---------------------------------------------------------------------------

def get_next_page_url(
    soup: BeautifulSoup,
    current_url: str,
) -> str | None:
    """
    Find the next page URL from a paginated category page.

    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML of the current category page.

    current_url : str
        Absolute URL of the current page.

    Returns
    -------
    str | None
        Absolute URL of the next page, or None when the current page
        is the final page.
    """

    # The website places the pagination link inside:
    # <li class="next"><a href="...">next</a></li>
    next_link = soup.select_one("li.next a")

    # No next link means this is the final page.
    if not next_link:
        return None

    # Convert the relative next-page URL into an absolute URL.
    return urljoin(current_url, next_link.get("href"))

# ---------------------------------------------------------------------------
# Category Book Scraping
# ---------------------------------------------------------------------------

def scrape_category(category_name: str, category_url: str) -> list[dict]:
    """
    Scrape all books from every page of a single category.

    Parameters
    ----------
    category_name : str
        Name of the category being scraped.

    category_url : str
        Absolute URL of the category's first page.

    Returns
    -------
    list[dict]
        List containing the raw book records collected from the
        category.
    """

    # Store the books collected from all pages of this category.
    books = []

    # Start with the category's first page.
    current_url = category_url

    # Continue until the category has no additional page.
    while current_url:

        # Fetch and parse the current category page.
        soup = fetch_page(current_url)

        # Locate every book card on the current page.
        products = soup.select("article.product_pod")

        # Extract each book from the page.
        for product in products:
            book = extract_book(product)

            # The category comes from the page context because it is
            # not stored inside the individual product card.
            book["category"] = category_name

            books.append(book)

        # Find the next page, or None if this was the final page.
        current_url = get_next_page_url(soup, current_url)

    return books

# ---------------------------------------------------------------------------
# Multi-Category Scraping
# ---------------------------------------------------------------------------

def scrape_categories(
    category_urls: dict[str, str],
) -> list[dict]:
    """
    Scrape all books from multiple categories.

    Parameters
    ----------
    category_urls : dict[str, str]
        Mapping of category names to their absolute starting URLs.

    Returns
    -------
    list[dict]
        Combined list of books from all requested categories.
    """

    # Store the combined results from every category.
    all_books = []

    # Process each category independently.
    for category_name, category_url in category_urls.items():

        print(f"Scraping category: {category_name}")

        # Scrape every page belonging to this category.
        category_books = scrape_category(
            category_name=category_name,
            category_url=category_url,
        )

        # Add the category's books to the overall dataset.
        all_books.extend(category_books)

        print(f"  Books collected: {len(category_books)}")

    return all_books


# ---------------------------------------------------------------------------
# Main Scraping Entry Point
# ---------------------------------------------------------------------------

def scrape_books(
    selected_categories: list[str],
) -> list[dict]:
    """
    Scrape all books from the selected categories.

    This function coordinates the complete scraping workflow:

    1. Fetch the website home page.
    2. Discover the requested category URLs.
    3. Convert category URLs to absolute URLs.
    4. Scrape all pages belonging to each category.
    5. Return the combined book records.

    Parameters
    ----------
    selected_categories : list[str]
        Category names to scrape.

    Returns
    -------
    list[dict]
        Combined raw book records.
    """

    # Fetch the website home page.
    soup = fetch_page(BASE_URL)

    # Discover the requested category URLs.
    category_urls = get_category_urls(
        soup=soup,
        selected_categories=selected_categories,
    )

    # Convert all category URLs from relative to absolute URLs.
    absolute_category_urls = {
        category: build_absolute_url(BASE_URL, relative_url)
        for category, relative_url in category_urls.items()
    }

    # Scrape all books across the selected categories.
    return scrape_categories(absolute_category_urls)

# ---------------------------------------------------------------------------
# Scraping Validation
# ---------------------------------------------------------------------------

REQUIRED_BOOK_FIELDS = {
    "title",
    "price",
    "star_rating",
    "availability",
    "category",
}


def validate_scraped_books(books: list[dict]) -> None:
    """
    Validate the scraped dataset against the Module 1 requirements.

    Validation checks:
    - At least 60 books are collected.
    - At least 3 categories are represented.
    - Every book contains the required fields.

    Parameters
    ----------
    books : list[dict]
        Scraped book records.

    Raises
    ------
    ValueError
        If any required validation fails.
    """

    # Requirement: the final dataset must contain at least 60 books.
    if len(books) < 60:
        raise ValueError(
            f"Scraping requirement failed: "
            f"expected at least 60 books, found {len(books)}."
        )

    # Extract unique non-empty category names.
    categories = {
        book["category"]
        for book in books
        if book.get("category")
    }

    # Requirement: books must come from at least 3 categories.
    if len(categories) < 3:
        raise ValueError(
            f"Scraping requirement failed: "
            f"expected at least 3 categories, found {len(categories)}."
        )

    # Check that every book contains all required fields.
    for index, book in enumerate(books, start=1):
        missing_fields = REQUIRED_BOOK_FIELDS - book.keys()

        if missing_fields:
            raise ValueError(
                f"Book record {index} is missing fields: "
                f"{sorted(missing_fields)}"
            )


# ---------------------------------------------------------------------------
# Raw Data Export
# ---------------------------------------------------------------------------

def save_raw_books(
    books: list[dict],
    output_path: str,
) -> None:
    """
    Save the raw scraped book records to a CSV file.

    Parameters
    ----------
    books : list[dict]
        Validated raw book records.

    output_path : str
        Destination path for the CSV file.
    """

    # Define the columns in the same order as the scraped dataset.
    fieldnames = [
        "title",
        "price",
        "star_rating",
        "availability",
        "category",
    ]

    # Open the output file using UTF-8 encoding so that book titles
    # and other text are preserved correctly.
    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        # Write the CSV header.
        writer.writeheader()

        # Write every scraped book record.
        writer.writerows(books)

