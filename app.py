import streamlit as st
from fetch_news import fetch_news
from ai_brief import generate_ai_brief
from datetime import datetime


# Page configuration
st.set_page_config(
    page_title="Vinoth's Daily News",
    page_icon="📰",
    layout="wide"
)

# App title
st.title("📰 Vinoth's Daily News")

# Current date
today_date = datetime.now().strftime("%d %B %Y")

# Refresh button
refresh = st.button("🔄 Refresh News")

# Last refreshed timestamp
refresh_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

st.caption(f"Latest updated news for {today_date}")
st.caption(f"Last refreshed: {refresh_time} IST")

# Fetch news with loading spinner
with st.spinner("Fetching latest headlines..."):

    news = fetch_news(today_date)

# Generate AI Brief
ai_brief = generate_ai_brief(news)

# Display AI Brief
st.subheader("🧠 Today's AI News Brief")

for line in ai_brief:
    st.write(line)

st.write("---")

# Display categorized news
for category, articles in news.items():

    # Sort latest-first
    sorted_articles = sorted(
        articles,
        key=lambda x: datetime.strptime(
            x["timestamp"],
            "%d %b %Y, %I:%M %p"
        ),
        reverse=True
    )

    with st.expander(
        f"{category} News ({len(sorted_articles)})",
        expanded=False
    ):

        if sorted_articles:

            for i, article in enumerate(sorted_articles, start=1):

                # Extract only time portion
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
