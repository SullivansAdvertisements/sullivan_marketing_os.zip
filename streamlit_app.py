import json
from datetime import datetime
from pathlib import Path
import base64

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.calculations import recommend_platforms, budget_split, estimate_metrics, health_score
from utils.exporters import export_csv, export_pdf, save_plan_text
from integrations.google_trends import get_google_trends, TIMEFRAME_OPTIONS
from integrations.status import integration_statuses
from creative.generator import create_creative
from campaign_builders.meta_builder import build_meta_plan
from campaign_builders.google_youtube_builder import build_google_youtube_plan
from campaign_builders.spotify_builder import build_spotify_plan

st.set_page_config(
    page_title="Sullivan's Innovative Marketing OS — Live",
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
    background-image: linear-gradient(180deg, rgba(3,8,5,.82), rgba(3,8,5,.94)), url("{bg}");
    background-size: cover; background-attachment: fixed; background-position: center;
}}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; }}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(6,19,13,.96), rgba(8,33,22,.94));
    border-right: 1px solid rgba(212,175,55,.32);
}}
.hero {{
    background: linear-gradient(135deg, rgba(6,19,13,.72), rgba(18,55,36,.66));
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
}}
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
    st.markdown("### Live Campaign Inputs")
    st.caption("Live-only build. No demo mode.")

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
  <div class="hero-title">Live Digital Marketing Beast</div>
  <div class="hero-sub">
    Sullivan’s Innovative Marketing OS for live research, OpenAI creative, campaign planning, 
    Spotify/music promotion, Meta/IG Ads, Google Search, YouTube Ads, and optimization.
  </div>
  <div style="margin-top:14px;">
    <span class="gold-pill">Live-Only Build</span>
    <span class="gold-pill">Working Google Trends Fallback</span>
    <span class="gold-pill">No Demo Mode</span>
    <span class="gold-pill">Luxury Gold + Deep Green UI</span>
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

    st.subheader("Platform Budget Split")
    st.dataframe(split_df, use_container_width=True)
    if not split_df.empty:
        st.plotly_chart(px.pie(split_df, names="Platform", values="Budget", hole=.46, title="Budget Allocation"), use_container_width=True)

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
        st.warning("Below $500: keep it tight. One offer, one market, one main platform, one backup platform.")
    elif budget < 2000:
        st.info("Starter Growth Plan: 2–3 platforms, 2 creative angles, 48–72 hour optimization checkpoints.")
    else:
        st.success("Aggressive Growth Plan: use cold testing, retargeting, and creative rotation across all top platforms.")

with tabs[2]:
    st.header("Live Google Trends Research Center")
    st.write("Uses pytrends first. If pytrends is blocked or rate-limited, it automatically uses live Google autocomplete suggestions. No demo data.")

    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        keyword = st.text_input("Main keyword", value=niche)
        extra_keywords = st.text_area("Optional comparison keywords, comma-separated. Max 4 extra.", value="")
    with col2:
        tf_label = st.selectbox("Timeframe", list(TIMEFRAME_OPTIONS.keys()), index=2)
        geo = st.text_input("Geo code", value="", help="Blank = worldwide for pytrends. US = United States, GB = United Kingdom.")
    with col3:
        max_results = st.slider("Max results", min_value=10, max_value=100, value=50, step=10)

    if st.button("Run Live Google Trends Research"):
        with st.spinner("Running live Google Trends / fallback research..."):
            try:
                st.session_state["research"] = get_google_trends(
                    keyword=keyword,
                    timeframe=TIMEFRAME_OPTIONS[tf_label],
                    geo=geo.strip(),
                    max_results=max_results,
                    extra_keywords=extra_keywords,
                    allow_fallback=True,
                )
                status = st.session_state["research"].get("status", "")
                message = st.session_state["research"].get("message", "Research loaded.")
                if status == "live_pytrends":
                    st.success(message)
                else:
                    st.warning(message)
            except Exception as e:
                st.error(str(e))

    research = st.session_state["research"]
    if research:
        status = research.get("status", "")
        message = research.get("message", "")
        if status == "live_pytrends":
            st.success(message)
        elif status == "live_fallback":
            st.warning(message)
            if research.get("pytrends_error"):
                with st.expander("Pytrends error details"):
                    st.code(str(research.get("pytrends_error")))

        iot = research.get("interest_over_time", pd.DataFrame())
        top = research.get("related_top", pd.DataFrame())
        rising = research.get("related_rising", pd.DataFrame())
        region = research.get("regional_interest", pd.DataFrame())
        yt = research.get("youtube_ideas", pd.DataFrame())

        st.subheader("Interest Over Time")
        st.dataframe(iot, use_container_width=True)
        if isinstance(iot, pd.DataFrame) and not iot.empty and "date" in iot.columns:
            chart_cols = [c for c in iot.columns if c not in ["date", "data_note"]]
            if chart_cols:
                st.line_chart(iot.set_index("date")[chart_cols])

        a, b = st.columns(2)
        with a:
            st.subheader("Top Related Queries")
            st.dataframe(top, use_container_width=True)
        with b:
            st.subheader("Rising Searches")
            st.dataframe(rising, use_container_width=True)

        st.subheader("Regional Interest")
        st.dataframe(region, use_container_width=True)

        st.subheader("YouTube Search & Video Ideas")
        st.dataframe(yt, use_container_width=True)

        if isinstance(top, pd.DataFrame) and not top.empty:
            csv_path = export_csv(top, "live_google_trends_related_queries.csv")
            st.download_button("Download Related Queries CSV", data=open(csv_path, "rb"), file_name="live_google_trends_related_queries.csv")

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
    st.info("Live publishing is not automatic in this build. Keep campaign creation paused until tracking, audience, budget, and policy checks are confirmed.")

with tabs[5]:
    st.header("Google / YouTube Ads Builder")
    keywords = []
    top = st.session_state.get("research", {}).get("related_top", pd.DataFrame())
    if isinstance(top, pd.DataFrame) and "query" in top.columns:
        keywords = top["query"].dropna().astype(str).head(12).tolist()
    st.json(build_google_youtube_plan(inputs, keywords, st.session_state.get("creative", "")))

with tabs[6]:
    st.header("Creative Studio")
    st.write("Live OpenAI only. Add OPENAI_API_KEY in Streamlit secrets to generate creative.")
    tone = st.selectbox("Creative Tone", ["luxury", "aggressive", "emotional", "viral", "professional", "streetwear", "music promo", "local business", "e-commerce"])
    if st.button("Generate Live OpenAI Creative Pack"):
        with st.spinner("Generating premium creative with OpenAI..."):
            try:
                st.session_state["creative"] = create_creative(inputs, tone)
                st.success("Creative pack generated.")
            except Exception as e:
                st.error(str(e))
    if st.session_state["creative"]:
        st.text_area("Generated Creative", st.session_state["creative"], height=440)

with tabs[7]:
    st.header("Campaign Development Engine")
    if st.button("Build Complete Live Campaign Plan"):
        keywords = []
        top = st.session_state.get("research", {}).get("related_top", pd.DataFrame())
        if isinstance(top, pd.DataFrame) and "query" in top.columns:
            keywords = top["query"].dropna().astype(str).head(12).tolist()
        full_plan = {
            "brand": "Sullivan's Innovative Marketing OS",
            "build": "live_only",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "inputs": inputs,
            "recommended_platforms": platforms,
            "budget_split": split_df.to_dict(orient="records"),
            "estimated_metrics": metrics_df.to_dict(orient="records"),
            "research_status": st.session_state.get("research", {}).get("status", "not_run"),
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
        pdf_path = export_pdf("Sullivan's Innovative Marketing OS Live Campaign Plan", st.session_state["plan_text"], "live_campaign_plan.pdf")
        csv_path = export_csv(metrics_df, "live_campaign_metrics.csv")
        st.download_button("Download Campaign Plan PDF", data=open(pdf_path, "rb"), file_name="live_campaign_plan.pdf")
        st.download_button("Download Metrics CSV", data=open(csv_path, "rb"), file_name="live_campaign_metrics.csv")

with tabs[8]:
    st.header("Metrics & Optimization")
    st.data_editor(metrics_df.copy(), use_container_width=True, num_rows="dynamic")
    st.markdown("""
**CPC:** cost per click.  
**CPM:** cost per 1,000 impressions.  
**CTR:** click-through rate.  
**CPA:** cost per conversion/action.  
**ROAS:** revenue divided by ad spend.  
**Budget pacing:** whether your spend is too slow, on track, or burning too fast.
""")
    st.success("Scale winners with strong CTR and low CPA. Cut or rewrite weak ads before increasing budget.")
