import streamlit as st
from fetch_news import fetch_news
from datetime import datetime


# Page config
st.set_page_config(
    page_title="Vinoth's Daily News",
    page_icon="📰",
    layout="wide"
)

# Title
st.title("📰 Vinoth's Daily News")

# Current date
today_date = datetime.now().strftime("%d %B %Y")

# Refresh button
refresh = st.button("🔄 Refresh News")

# Last refreshed timestamp
refresh_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

st.caption(f"Latest updated news for {today_date}")
st.caption(f"Last refreshed: {refresh_time} IST")

# Loading spinner
with st.spinner("Fetching latest headlines..."):

    news = fetch_news(today_date)

# Display categories
for category, articles in news.items():

    # Sort latest first
    sorted_articles = sorted(
        articles,
        key=lambda x: x["timestamp"],
        reverse=True
    )

    with st.expander(f"{category} News ({len(sorted_articles)})", expanded=False):

        if sorted_articles:

            for i, article in enumerate(sorted_articles, start=1):

                time_only = article["timestamp"].split(",")[1].strip()

                st.markdown(
                    f"""
                    **{i}. {article['title']}**  
                    🕒 {time_only} | [🔗 Open]({article['link']})
                    """
                )

                st.write("---")

        else:
            st.write("No headlines found.")
