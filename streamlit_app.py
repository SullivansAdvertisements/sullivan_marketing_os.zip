import json
from datetime import datetime
from pathlib import Path
import base64

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.calculations import recommend_platforms, budget_split, estimate_metrics, health_score
from utils.exporters import export_csv, export_pdf, save_plan_text
from integrations.google_trends import get_google_trends, demo_trends, TIMEFRAME_OPTIONS
from integrations.status import integration_statuses
from creative.generator import create_creative
from campaign_builders.meta_builder import build_meta_plan
from campaign_builders.google_youtube_builder import build_google_youtube_plan
from campaign_builders.spotify_builder import build_spotify_plan

st.set_page_config(
    page_title="Sullivan's Innovative Marketing OS",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

def asset_data_uri(path: str) -> str:
    p = Path(path)
    data = p.read_bytes()
    mime = "image/svg+xml" if p.suffix.lower() == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

bg = asset_data_uri("assets/luxury_floral_background.svg")
logo = asset_data_uri("assets/logo.svg")

st.markdown(f"""
<style>
.stApp {{
    background-image:
      linear-gradient(180deg, rgba(3,8,5,.82), rgba(3,8,5,.92)),
      url("{bg}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; }}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(6,19,13,.94), rgba(8,33,22,.92));
    border-right: 1px solid rgba(212,175,55,.32);
}}
.lux-card {{
    background: linear-gradient(135deg, rgba(8,30,20,.82), rgba(16,42,29,.72));
    border: 1px solid rgba(212,175,55,.30);
    box-shadow: 0 18px 60px rgba(0,0,0,.42), inset 0 0 28px rgba(212,175,55,.06);
    border-radius: 26px;
    padding: 22px;
    backdrop-filter: blur(12px);
}}
.hero {{
    background: linear-gradient(135deg, rgba(6,19,13,.70), rgba(18,55,36,.64));
    border: 1px solid rgba(255,235,160,.32);
    box-shadow: 0 25px 80px rgba(0,0,0,.50);
    border-radius: 34px;
    padding: 28px;
    margin-bottom: 22px;
}}
.hero-title {{
    font-family: Georgia, serif;
    font-size: clamp(2rem, 4vw, 4.2rem);
    line-height: 1;
    background: linear-gradient(90deg, #fff8cf, #d4af37, #7ddba9);
    -webkit-background-clip: text;
    color: transparent;
    font-weight: 900;
}}
.hero-sub {{ color: #efe7c8; font-size: 1.05rem; max-width: 920px; }}
.gold-pill {{
    display: inline-block; padding: 7px 12px; border-radius: 999px;
    border: 1px solid rgba(212,175,55,.45);
    background: rgba(212,175,55,.10); color: #fff5bd; margin: 3px 5px 3px 0;
}}
div[data-testid="stMetric"] {{
    background: linear-gradient(135deg, rgba(10,44,29,.88), rgba(5,17,11,.86));
    border: 1px solid rgba(212,175,55,.28);
    border-radius: 20px;
    padding: 16px;
}}
.stButton>button, .stDownloadButton>button {{
    background: linear-gradient(135deg, #fff1a8, #d4af37, #806017);
    color: #06130d;
    border: 0;
    border-radius: 14px;
    font-weight: 800;
    box-shadow: 0 10px 25px rgba(212,175,55,.20);
}}
.stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
.stTabs [data-baseweb="tab"] {{
    background: rgba(6,19,13,.72);
    border: 1px solid rgba(212,175,55,.20);
    border-radius: 14px;
    padding: 10px 14px;
}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image(logo, use_container_width=True)
    st.markdown("### Campaign Command Center")
    mode = st.radio("Data Mode", ["Demo Mode", "Live Mode"], help="Live Mode uses real APIs only when keys are configured.")
    st.divider()

    niche = st.text_input("Niche / Genre", value="Hip-hop music promotion")
    name = st.text_input("Artist / Brand Name", value="Sullivan Demo Artist")
    offer = st.text_input("Offer / Release / Product", value="New single + music video")
    goal = st.selectbox("Campaign Goal", ["traffic", "engagement", "conversions", "video views", "leads", "awareness"])
    budget = st.number_input("Total Budget ($)", min_value=50.0, value=1500.0, step=50.0)
    location = st.text_input("Target Location", value="United States, Canada, United Kingdom")
    audience = st.text_area("Audience", value="Fans of independent hip-hop, music video viewers, Spotify listeners")
    timeframe = st.text_input("Timeframe", value="30 days")

    st.divider()
    st.markdown("### Live Integration Status")
    for k, ready in integration_statuses().items():
        st.caption(("✅ " if ready else "⚠️ ") + k)

inputs = {
    "niche": niche, "name": name, "offer": offer, "goal": goal,
    "budget": budget, "location": location, "audience": audience, "timeframe": timeframe
}

if "research" not in st.session_state: st.session_state["research"] = {}
if "creative" not in st.session_state: st.session_state["creative"] = ""
if "plan_text" not in st.session_state: st.session_state["plan_text"] = ""

platforms = recommend_platforms(niche, goal)
split_df = budget_split(budget, platforms)
metrics_df = estimate_metrics(split_df)
score, actions = health_score(budget, bool(st.session_state["research"]), bool(st.session_state["creative"]), len(platforms))

st.markdown(f"""
<div class="hero">
  <img src="{logo}" style="max-width:460px;width:100%;margin-bottom:14px;">
  <div class="hero-title">Luxury Digital Marketing Beast</div>
  <div class="hero-sub">
    A premium, beginner-friendly Marketing OS for research, campaign strategy, creative generation,
    Spotify/music promotion, Meta/IG Ads, Google Search, YouTube Ads, and optimization.
  </div>
  <div style="margin-top:14px;">
    <span class="gold-pill">Gold + Deep Green Brand System</span>
    <span class="gold-pill">Google Trends Max Results</span>
    <span class="gold-pill">OpenAI Creative Studio</span>
    <span class="gold-pill">Exportable Campaign Plans</span>
  </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "Dashboard", "Strategy Builder", "Google Trends Research", "Spotify / Music Planner",
    "Meta / Instagram Ads", "Google / YouTube Ads", "Creative Studio",
    "Campaign Development Engine", "Metrics & Optimization"
])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Budget", f"${budget:,.0f}")
    c2.metric("Platforms", len(platforms))
    c3.metric("Health Score", f"{score}/100")
    c4.metric("Timeframe", timeframe)

    st.markdown('<div class="lux-card">', unsafe_allow_html=True)
    st.subheader("Platform Budget Split")
    st.dataframe(split_df, use_container_width=True)
    if not split_df.empty:
        st.plotly_chart(px.pie(split_df, names="Platform", values="Budget", hole=.46, title="Luxury Budget Allocation"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Estimated Campaign Overview")
    st.dataframe(metrics_df, use_container_width=True)

    st.subheader("What should I do next?")
    for item in actions:
        st.info(item)

with tabs[1]:
    st.header("Strategy Builder")
    st.success(f"Recommended platforms: {', '.join(platforms)}")
    st.dataframe(split_df, use_container_width=True)
    if budget < 500:
        st.warning("Below $500: keep it very tight. One offer, one market, one main platform, one backup platform.")
    elif budget < 2000:
        st.info("Starter Growth Plan: 2–3 platforms, 2 creative angles, 48–72 hour optimization checkpoints.")
    else:
        st.success("Aggressive Growth Plan: use cold testing, retargeting, and creative rotation across all top platforms.")

with tabs[2]:
    st.header("Google Trends Research Center — Max Results")
    st.write("Clean trend research for keywords, rising searches, regional demand, and YouTube ideas.")
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        keyword = st.text_input("Main keyword", value=niche)
        extra_keywords = st.text_area("Optional comparison keywords, comma-separated. Max 4 extra.", value="", help="Google Trends supports 5 terms per request.")
    with col2:
        tf_label = st.selectbox("Timeframe", list(TIMEFRAME_OPTIONS.keys()), index=2)
        geo = st.text_input("Geo code", value="", help="Blank = worldwide, US = United States, GB = United Kingdom.")
    with col3:
        max_results = st.slider("Max results", min_value=10, max_value=100, value=50, step=10)
        st.caption("Higher results show more related/rising terms when Google returns them.")

    if st.button("Run Max Google Trends Research"):
        with st.spinner("Building clean trend tables..."):
            try:
                if mode == "Demo Mode":
                    st.session_state["research"] = demo_trends(keyword, max_results)
                    st.warning("Demo Mode: sample trend data is clearly marked and safe for testing.")
                else:
                    st.session_state["research"] = get_google_trends(
                        keyword=keyword,
                        timeframe=TIMEFRAME_OPTIONS[tf_label],
                        geo=geo.strip(),
                        max_results=max_results,
                        extra_keywords=extra_keywords
                    )
                    st.success("Live Google Trends research loaded.")
            except Exception as e:
                st.error(str(e))

    research = st.session_state["research"]
    if research:
        iot = research.get("interest_over_time", pd.DataFrame())
        top = research.get("related_top", pd.DataFrame())
        rising = research.get("related_rising", pd.DataFrame())
        region = research.get("regional_interest", pd.DataFrame())
        yt = research.get("youtube_ideas", pd.DataFrame())

        st.subheader("Interest Over Time")
        st.dataframe(iot, use_container_width=True)
        if isinstance(iot, pd.DataFrame) and not iot.empty and "date" in iot.columns:
            chart_df = iot.set_index("date")
            st.line_chart(chart_df)

        colA, colB = st.columns(2)
        with colA:
            st.subheader("Top Related Queries")
            st.dataframe(top, use_container_width=True)
        with colB:
            st.subheader("Rising Searches")
            st.dataframe(rising, use_container_width=True)

        st.subheader("Regional Interest")
        st.dataframe(region, use_container_width=True)

        st.subheader("YouTube Search & Video Ideas")
        st.dataframe(yt, use_container_width=True)

        if not top.empty:
            csv_path = export_csv(top, "google_trends_related_queries.csv")
            st.download_button("Download Related Queries CSV", data=open(csv_path, "rb"), file_name="google_trends_related_queries.csv")

with tabs[3]:
    st.header("Spotify / Music Promotion Planner")
    plan = build_spotify_plan(inputs)
    for k, v in plan.items():
        st.subheader(k)
        st.write(v)
    st.subheader("Playlist Submission Tracker")
    tracker = pd.DataFrame(columns=["Curator/Playlist", "Genre Fit", "Submission Date", "Status", "Result", "Notes"])
    st.data_editor(tracker, use_container_width=True, num_rows="dynamic")

with tabs[4]:
    st.header("Meta / Instagram Ads Builder")
    st.json(build_meta_plan(inputs, st.session_state.get("creative", "")))
    st.info("Campaigns should stay paused for review until tracking, audience, budget, and policy checks are confirmed.")

with tabs[5]:
    st.header("Google / YouTube Ads Builder")
    keywords = []
    top = st.session_state.get("research", {}).get("related_top", pd.DataFrame())
    if isinstance(top, pd.DataFrame) and "query" in top.columns:
        keywords = top["query"].dropna().astype(str).head(12).tolist()
    st.json(build_google_youtube_plan(inputs, keywords, st.session_state.get("creative", "")))

with tabs[6]:
    st.header("Creative Studio")
    tone = st.selectbox("Creative Tone", ["luxury", "aggressive", "emotional", "viral", "professional", "streetwear", "music promo", "local business", "e-commerce"])
    if st.button("Generate Premium Creative Pack"):
        with st.spinner("Generating premium creative..."):
            try:
                st.session_state["creative"] = create_creative(inputs, tone, demo_mode=(mode == "Demo Mode"))
                st.success("Creative pack generated.")
            except Exception as e:
                st.error(str(e))
    if st.session_state["creative"]:
        st.text_area("Generated Creative", st.session_state["creative"], height=440)

with tabs[7]:
    st.header("Campaign Development Engine")
    if st.button("Build Complete Luxury Campaign Plan"):
        keywords = []
        top = st.session_state.get("research", {}).get("related_top", pd.DataFrame())
        if isinstance(top, pd.DataFrame) and "query" in top.columns:
            keywords = top["query"].dropna().astype(str).head(12).tolist()
        full_plan = {
            "brand": "Sullivan's Innovative Marketing OS",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "inputs": inputs,
            "recommended_platforms": platforms,
            "budget_split": split_df.to_dict(orient="records"),
            "estimated_metrics": metrics_df.to_dict(orient="records"),
            "spotify_music": build_spotify_plan(inputs),
            "meta_instagram": build_meta_plan(inputs, st.session_state.get("creative", "")),
            "google_youtube": build_google_youtube_plan(inputs, keywords, st.session_state.get("creative", "")),
            "next_actions": actions,
            "launch_checklist": [
                "Confirm tracking and conversion events.",
                "Confirm landing page speed on mobile.",
                "Review ad policies before publishing.",
                "Launch with controlled budgets first.",
                "Optimize after 48–72 hours of real spend."
            ],
        }
        st.session_state["plan_text"] = json.dumps(full_plan, indent=2)

    if st.session_state["plan_text"]:
        st.code(st.session_state["plan_text"], language="json")
        save_plan_text(st.session_state["plan_text"])
        pdf_path = export_pdf("Sullivan's Innovative Marketing OS Campaign Plan", st.session_state["plan_text"], "luxury_campaign_plan.pdf")
        csv_path = export_csv(metrics_df, "luxury_campaign_metrics.csv")
        st.download_button("Download Campaign Plan PDF", data=open(pdf_path, "rb"), file_name="luxury_campaign_plan.pdf")
        st.download_button("Download Metrics CSV", data=open(csv_path, "rb"), file_name="luxury_campaign_metrics.csv")

with tabs[8]:
    st.header("Metrics & Optimization")
    editable = st.data_editor(metrics_df.copy(), use_container_width=True, num_rows="dynamic")
    st.markdown("""
**CPC:** cost per click.  
**CPM:** cost per 1,000 impressions.  
**CTR:** click-through rate.  
**CPA:** cost per conversion/action.  
**ROAS:** revenue divided by ad spend.  
**Budget pacing:** whether your spend is too slow, on track, or burning too fast.
""")
    st.success("Scale winners with strong CTR and low CPA. Cut or rewrite weak ads before increasing budget.")
