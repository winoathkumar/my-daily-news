import streamlit as st
from fetch_news import fetch_news
from ai_brief import generate_ai_brief
from datetime import datetime


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Vinoth's Daily News",
    page_icon="📰",
    layout="wide"
)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("📰 Vinoth's Daily News")

today_date = datetime.now().strftime("%d %B %Y")
from datetime import timedelta

ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)

refresh_time = ist_now.strftime("%d %b %Y, %I:%M %p")

col1, col2 = st.columns([4, 1])

with col1:
    st.caption(f"Latest updated news for {today_date}")
    st.caption(f"🕒 Last refreshed: {refresh_time} IST")

with col2:
    refresh = st.button("🔄 Refresh")


# ---------------------------------------------------
# FETCH NEWS
# ---------------------------------------------------

with st.spinner("Fetching latest headlines..."):

    news = fetch_news(today_date)


# ---------------------------------------------------
# AI BRIEF SECTION
# ---------------------------------------------------

ai_brief = generate_ai_brief(news)

st.markdown("## 🧠 Today's AI Brief")

for line in ai_brief:
    st.markdown(f"- {line}")

st.markdown("---")


# ---------------------------------------------------
# CATEGORY TABS
# ---------------------------------------------------

tabs = st.tabs([
    "🏙 Bengaluru",
    "🌆 Karnataka",
    "🇮🇳 National",
    "🌍 World",
    "⚽ Sports"
])


category_mapping = {
    "🏙 Bengaluru": "Bengaluru",
    "🌆 Karnataka": "Karnataka",
    "🇮🇳 National": "National",
    "🌍 World": "World",
    "⚽ Sports": "Sports"
}


# ---------------------------------------------------
# DISPLAY TAB CONTENT
# ---------------------------------------------------

for tab, (tab_name, category) in zip(tabs, category_mapping.items()):

    with tab:

        articles = news.get(category, [])

        # Sort latest first
        sorted_articles = sorted(
            articles,
            key=lambda x: datetime.strptime(
                x["timestamp"],
                "%d %b %Y, %I:%M %p"
            ),
            reverse=True
        )

        if sorted_articles:

            for article in sorted_articles:

                time_only = article["timestamp"].split(",")[1].strip()

                # News card
                st.markdown(
                    f"""
                    <div style="
                        padding:15px;
                        border-radius:12px;
                        border:1px solid #E0E0E0;
                        margin-bottom:15px;
                        background-color:#FFFFFF;
                        box-shadow:0 2px 6px rgba(0,0,0,0.05);
                    ">

                    <div style="
                        font-size:18px;
                        font-weight:600;
                        margin-bottom:10px;
                        color:#111111;
                    ">
                        {article['title']}
                    </div>

                    <div style="
                        font-size:14px;
                        color:gray;
                        margin-bottom:10px;
                    ">
                        🕒 {time_only}
                    </div>

                    <a href="{article['link']}" target="_blank"
                       style="
                           text-decoration:none;
                           color:#1f77b4;
                           font-weight:600;
                       ">
                       🔗 Read Article
                    </a>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.info("No headlines found.")
