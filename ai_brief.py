def generate_ai_brief(news):

    brief_lines = []

    category_templates = {
        "Bengaluru": "Local Bengaluru headlines focused on",
        "Karnataka": "Karnataka news highlighted",
        "National": "National developments included",
        "World": "Global headlines focused on",
        "Sports": "Sports news highlighted"
    }

    for category, articles in news.items():

        if not articles:
            continue

        # Take top 2 headlines
        top_headlines = [article["title"] for article in articles[:2]]

        combined = " | ".join(top_headlines)

        summary = (
            f"• {category_templates.get(category, category)} "
            f"{combined.lower()}."
        )

        brief_lines.append(summary)

    return brief_lines