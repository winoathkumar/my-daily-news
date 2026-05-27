import streamlit as st
from fetch_news import fetch_news
from ai_brief import generate_ai_brief
from datetime import datetime, timedelta


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Vinoth's Daily News",
    page_icon="📰",
    layout="wide"
)

# Smooth scrolling
st.markdown(
    """
    <style>
    html {
        scroll-behavior: smooth;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# IST TIME
# ---------------------------------------------------

ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)

today_date = ist_now.strftime("%d %B %Y")

refresh_time = ist_now.strftime("%d %b %Y, %I:%M %p")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    "<h1 id='vinoths-daily-news'>📰 Vinoth's Daily News</h1>",
    unsafe_allow_html=True
)

left_col, right_col = st.columns([5, 1])

with left_col:
    st.caption(f"Latest updated news for {today_date}")
    st.caption(f"🕒 Last refreshed: {refresh_time} IST")

with right_col:
    refresh = st.button("🔄 Refresh")


# ---------------------------------------------------
# DARK THEME
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA !important;
    }

    p, div, span, label {
        color: #E0E0E0 !important;
    }

    a {
        color: #4DA3FF !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

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
    st.markdown(line)

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

        # Sort latest-first
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

                # News card UI
                st.markdown(
                    f"""
                    <div style="
                        padding:15px;
                        border-radius:12px;
                        border:1px solid #E0E0E0;
                        margin-bottom:15px;
                        background-color:#1E1E1E;
                        box-shadow:0 2px 6px rgba(0,0,0,0.05);
                    ">

                    <div style="
                        font-size:18px;
                        font-weight:600;
                        margin-bottom:10px;
                        color:#FAFAFA;
                    ">
                        {article['title']}
                    </div>

                    <div style="
                        font-size:14px;
                        color:#BBBBBB;
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

        # Back to Top
        st.markdown("---")

        st.markdown(
            """
            <div style='text-align:center; padding:10px;'>
                <a href='#vinoths-daily-news'
                   style='text-decoration:none;
                          font-weight:600;
                          font-size:16px;'>
                    ⬆ Back to Top
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
