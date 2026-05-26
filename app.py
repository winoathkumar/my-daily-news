import streamlit as st
from fetch_news import fetch_news
from datetime import date


# Page config
st.set_page_config(
    page_title="Vinoth's Daily News Agent",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Vinoth's Daily News Agent")
st.write("Select a date and fetch categorized headlines")


# Date input
selected_date = st.date_input(
    "Choose a date",
    value=date.today()
)

formatted_date = selected_date.strftime("%d %B %Y")


# Button
if st.button("Fetch Headlines"):

    st.write(f"Fetching headlines for: **{formatted_date}**")

    news = fetch_news(formatted_date)

    for category, articles in news.items():

        # Collapsible section
        with st.expander(f"{category} News ({len(articles)})", expanded=False):

            if articles:

                for i, article in enumerate(articles, start=1):

                    # Extract only time
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