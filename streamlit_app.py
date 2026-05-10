import base64
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

from integrations.google_trends import get_google_trends, TIMEFRAME_OPTIONS
from integrations.status import integration_statuses
from creative.generator import create_creative
from utils.calculations import recommend_platforms, budget_split

st.set_page_config(
    page_title="Sullivan's Innovative Marketing OS",
    page_icon="✨",
    layout="wide",
)

def data_uri(path):
    p = Path(path)
    mime = "image/svg+xml"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"

bg = data_uri("assets/bg.svg")
logo = data_uri("assets/logo.svg")

st.markdown(f"""
<style>
.stApp {{
background-image:
linear-gradient(rgba(3,8,5,.82), rgba(3,8,5,.92)),
url("{bg}");
background-size:cover;
background-attachment:fixed;
}}
.hero {{
padding:30px;
border-radius:30px;
background:rgba(8,24,17,.72);
border:1px solid rgba(212,175,55,.28);
}}
.hero-title {{
font-size:4rem;
font-family:Georgia;
font-weight:900;
background:linear-gradient(90deg,#fff7c4,#d4af37,#7ddba9);
-webkit-background-clip:text;
color:transparent;
}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image(logo, use_container_width=True)
    st.markdown("### Campaign Inputs")

    niche = st.text_input("Niche", "Hip-hop music promotion")
    brand = st.text_input("Artist / Brand", "Sullivan Demo")
    offer = st.text_input("Offer", "New single + music video")
    audience = st.text_area("Audience", "Hip-hop fans, Spotify listeners, music video viewers")
    budget = st.number_input("Budget", value=1500.0, step=50.0)

    st.divider()

    st.markdown("### Integration Status")

    for k,v in integration_statuses().items():
        st.caption(("✅ " if v else "⚠️ ") + k)

st.markdown(f"""
<div class="hero">
<img src="{logo}" style="max-width:500px;width:100%;">
<div class="hero-title">SERPAPI Marketing Beast</div>
<p style="color:#f4e8b8;font-size:1.1rem;">
Live SERPAPI Google Trends + OpenAI + Meta + Google + YouTube campaign planning.
</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "Dashboard",
    "Google Trends Research",
    "Creative Studio",
])

platforms = recommend_platforms(niche)
split = budget_split(budget, platforms)

with tabs[0]:
    st.header("Dashboard")
    st.dataframe(split, use_container_width=True)

    st.plotly_chart(
        px.pie(split, names="Platform", values="Budget", hole=.45),
        use_container_width=True
    )

with tabs[1]:

    st.header("SERPAPI Google Trends")

    col1,col2,col3 = st.columns(3)

    with col1:
        keyword = st.text_input("Keyword", value=niche)

    with col2:
        geo = st.text_input("Geo", value="US")

    with col3:
        tf = st.selectbox(
            "Timeframe",
            list(TIMEFRAME_OPTIONS.keys()),
            index=2
        )

    if st.button("Run SERPAPI Trends Research"):

        with st.spinner("Loading SERPAPI trends..."):

            try:

                data = get_google_trends(
                    keyword=keyword,
                    geo=geo,
                    date=TIMEFRAME_OPTIONS[tf],
                )

                st.success("SERPAPI Google Trends loaded.")

                st.subheader("Interest Over Time")

                iot = data["interest_over_time"]

                st.dataframe(iot, use_container_width=True)

                if not iot.empty:
                    st.line_chart(iot.set_index("date"))

                st.subheader("Related Queries")

                rq = data["related_queries"]

                st.dataframe(rq, use_container_width=True)

                st.subheader("Regional Interest")

                reg = data["regional_interest"]

                st.dataframe(reg, use_container_width=True)

                st.subheader("YouTube Ideas")

                yt = data["youtube_ideas"]

                st.dataframe(yt, use_container_width=True)

            except Exception as e:

                st.error(str(e))

with tabs[2]:

    st.header("Creative Studio")

    tone = st.selectbox(
        "Tone",
        [
            "luxury",
            "aggressive",
            "viral",
            "professional",
            "music promo",
            "streetwear",
        ]
    )

    if st.button("Generate OpenAI Creative"):

        try:

            creative = create_creative(
                {
                    "niche": niche,
                    "offer": offer,
                    "audience": audience,
                    "budget": budget,
                },
                tone=tone,
            )

            st.text_area(
                "Generated Creative",
                creative,
                height=500,
            )

        except Exception as e:

            st.error(str(e))
