import requests
from datetime import datetime, timedelta


BASE_URL = "https://www.deccanherald.com/api/v1/collections"


def format_timestamp(timestamp_ms):
    """
    Converts UTC timestamp to IST
    """
    dt = datetime.utcfromtimestamp(timestamp_ms / 1000)
    dt = dt + timedelta(hours=5, minutes=30)

    return dt.strftime("%d %b %Y, %I:%M %p")


def get_date_only(timestamp_ms):
    """
    Returns date only in IST
    Example: 26 May 2026
    """
    dt = datetime.utcfromtimestamp(timestamp_ms / 1000)
    dt = dt + timedelta(hours=5, minutes=30)

    return dt.strftime("%d %B %Y")


def build_article_url(slug):
    return f"https://www.deccanherald.com/{slug}"


def fetch_collection(collection_name, limit=50):
    """
    Fetches stories from a DH API collection
    """

    url = (
        f"{BASE_URL}/{collection_name}"
        f"?limit={limit}&offset=0&item-type=story"
    )

    response = requests.get(url)

    print(f"Fetching {collection_name} → Status {response.status_code}")

    if response.status_code != 200:
        return []

    data = response.json()

    articles = []

    for item in data.get("items", []):

        story = item.get("story", {})

        headline = story.get("headline")
        published_at = story.get("published-at")
        slug = story.get("slug")

        if headline and published_at and slug:

            article = {
                "title": headline,
                "timestamp": format_timestamp(published_at),
                "date_only": get_date_only(published_at),
                "link": build_article_url(slug)
            }

            articles.append(article)

    return articles


def is_matching_date(article_date, selected_date):
    """
    Checks whether article date matches selected date
    """
    if not selected_date:
        return True

    return article_date.lower() == selected_date.lower()


def fetch_news(selected_date=None):
    """
    Final API-driven categorized news fetcher
    """

    categorized_news = {
        "Bengaluru": [],
        "Karnataka": [],
        "National": [],
        "World": [],
        "Sports": []
    }

    # Bengaluru-specific feed
    bengaluru_articles = fetch_collection("bengaluru-karnataka-india", limit=50)

    for article in bengaluru_articles:

        if not is_matching_date(article["date_only"], selected_date):
            continue

        link = article["link"].lower()

        if "/india/karnataka/bengaluru/" in link:
            categorized_news["Bengaluru"].append(article)

    # India feed → split into Karnataka + National
    india_articles = fetch_collection("india", limit=100)

    for article in india_articles:

        if not is_matching_date(article["date_only"], selected_date):
            continue

        link = article["link"].lower()

        if "/india/karnataka/" in link:

            if "/india/karnataka/bengaluru/" not in link:
                categorized_news["Karnataka"].append(article)

        else:
            categorized_news["National"].append(article)

    # World
    world_articles = fetch_collection("world", limit=50)

    for article in world_articles:

        if is_matching_date(article["date_only"], selected_date):
            categorized_news["World"].append(article)

    # Sports
    sports_articles = fetch_collection("sports", limit=50)

    for article in sports_articles:

        if is_matching_date(article["date_only"], selected_date):
            categorized_news["Sports"].append(article)

    return categorized_news