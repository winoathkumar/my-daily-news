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

st.caption(f"Latest updated news for {today_date}")

# Auto-fetch latest news
news = fetch_news(today_date)

# Display categories
for category, articles in news.items():

    with st.expander(f"{category} News ({len(articles)})", expanded=False):

        if articles:

            for i, article in enumerate(articles, start=1):

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
