import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.calculations import recommend_platforms, budget_split, estimate_metrics, health_score
from utils.exporters import export_csv, export_pdf, save_plan_text
from integrations.google_trends import get_google_trends
from integrations.meta_ads import meta_status
from integrations.google_ads import google_ads_status
from integrations.youtube import youtube_status
from integrations.spotify import spotify_status
from creative.generator import create_creative
from campaign_builders.meta_builder import build_meta_plan
from campaign_builders.google_youtube_builder import build_google_youtube_plan
from campaign_builders.spotify_builder import build_spotify_music_plan

st.set_page_config(
    page_title="Sullivan Marketing OS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# App styling
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
.metric-card {
    background: linear-gradient(135deg, #101C2E 0%, #13283E 100%);
    padding: 18px; border-radius: 18px; border: 1px solid rgba(255,255,255,.08);
}
.big-title {font-size: 2.2rem; font-weight: 800; line-height: 1.1;}
.small-muted {color: #A7B0C0; font-size: .95rem;}
.success-pill {background:#0f3b2f; padding:6px 10px; border-radius:999px;}
.warning-pill {background:#3b2c0f; padding:6px 10px; border-radius:999px;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🚀 Sullivan Marketing OS")
    st.caption("Digital Marketing Beast — beginner-friendly, real-data ready.")
    mode = st.radio("Data Mode", ["Demo Mode", "Live Mode"], help="Live Mode uses real APIs only when keys are configured.")
    st.session_state["mode"] = mode
    st.divider()

    st.markdown("### Campaign Inputs")
    niche = st.text_input("Niche / Genre", value="Hip-hop music promotion")
    name = st.text_input("Artist / Brand Name", value="Demo Artist")
    offer = st.text_input("Offer / Release / Product", value="New single + music video")
    goal = st.selectbox("Campaign Goal", ["traffic", "engagement", "conversions", "video views", "leads", "awareness"])
    budget = st.number_input("Total Budget ($)", min_value=50.0, value=1500.0, step=50.0)
    location = st.text_input("Target Location", value="United States, Canada, United Kingdom")
    audience = st.text_area("Audience", value="Fans of independent hip-hop, music video viewers, Spotify listeners")
    timeframe = st.text_input("Timeframe", value="30 days")

    inputs = {
        "niche": niche, "name": name, "offer": offer, "goal": goal,
        "budget": budget, "location": location, "audience": audience, "timeframe": timeframe
    }

    st.divider()
    st.markdown("### Integration Status")
    statuses = {
        "Meta": meta_status(),
        "Google Ads": google_ads_status(),
        "YouTube": youtube_status(),
        "Spotify": spotify_status(),
    }
    for label, status in statuses.items():
        icon = "✅" if status["ready"] else "⚠️"
        st.caption(f"{icon} {label}: {status['message']}")

# Shared state
if "research" not in st.session_state:
    st.session_state["research"] = {}
if "creative" not in st.session_state:
    st.session_state["creative"] = ""
if "plan_text" not in st.session_state:
    st.session_state["plan_text"] = ""

platforms = recommend_platforms(niche, goal)
split_df = budget_split(budget, platforms)
metrics_df = estimate_metrics(split_df)
score, actions = health_score(
    budget=budget,
    has_research=bool(st.session_state["research"]),
    has_creative=bool(st.session_state["creative"]),
    platforms=len(platforms),
)

tabs = st.tabs([
    "Dashboard",
    "Strategy Builder",
    "Research Center",
    "Spotify / Music Planner",
    "Meta / Instagram Ads",
    "Google / YouTube Ads",
    "Creative Studio",
    "Campaign Development Engine",
    "Metrics & Optimization",
    "Setup & Deployment",
])

with tabs[0]:
    st.markdown('<div class="big-title">Digital Marketing Beast Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<p class="small-muted">A clean command center for campaign research, planning, creative, and launch decisions.</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Budget", f"${budget:,.0f}")
    c2.metric("Platforms", len(platforms))
    c3.metric("Health Score", f"{score}/100")
    c4.metric("Timeframe", timeframe)

    st.subheader("Platform Budget Split")
    st.dataframe(split_df, use_container_width=True)
    if not split_df.empty:
        fig = px.pie(split_df, names="Platform", values="Budget", title="Budget Allocation")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Estimated Campaign Overview")
    st.dataframe(metrics_df, use_container_width=True)

    st.subheader("What should I do next?")
    for item in actions:
        st.info(item)

with tabs[1]:
    st.header("Strategy Builder")
    st.write("Enter your campaign details in the sidebar. The bot recommends channels, budget split, and next steps.")
    st.success(f"Recommended platforms: {', '.join(platforms)}")
    st.dataframe(split_df, use_container_width=True)

    if budget < 500:
        st.warning("For most paid campaigns, $500 is the minimum useful test budget. Below that, keep the campaign narrow.")
    elif 500 <= budget < 2000:
        st.info("Low-budget plan: test 2–3 audiences, 2 creative angles, and one clear conversion path.")
    else:
        st.success("Growth plan: split budget across proven audiences, retargeting, and new experiments.")

with tabs[2]:
    st.header("Research Center")
    st.write("Use Google Trends for keyword direction, regional interest, rising searches, and YouTube content ideas.")
    keyword = st.text_input("Research keyword", value=niche)
    timeframe_opt = st.selectbox("Google Trends timeframe", ["now 7-d", "today 1-m", "today 3-m", "today 12-m", "today 5-y"], index=2)
    geo = st.text_input("Geo code optional", value="", help="Use blank for worldwide, US for United States, GB for United Kingdom, etc.")

    if st.button("Run Google Trends Research"):
        if mode == "Demo Mode":
            dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="W")
            demo_interest = pd.DataFrame({"date": dates, keyword: [25, 30, 28, 40, 48, 55, 52, 63, 70, 66, 75, 82]})
            demo_related = pd.DataFrame({"query": [f"{keyword} playlist", f"{keyword} video", f"best {keyword}", f"new {keyword}"], "value": [100, 88, 71, 60]})
            demo_region = pd.DataFrame({"geoName": ["United States", "Canada", "United Kingdom", "Australia"], keyword: [100, 76, 68, 55]})
            st.session_state["research"] = {
                "interest_over_time": demo_interest,
                "related_top": demo_related,
                "related_rising": demo_related,
                "regional_interest": demo_region,
            }
            st.warning("Demo Mode is on. These are sample results clearly marked as demo data.")
        else:
            with st.spinner("Pulling live Google Trends data..."):
                try:
                    st.session_state["research"] = get_google_trends(keyword, timeframe_opt, geo)
                    st.success("Live Google Trends research loaded.")
                except Exception as e:
                    st.error(str(e))

    research = st.session_state["research"]
    if research:
        if not research.get("interest_over_time", pd.DataFrame()).empty:
            st.subheader("Interest Over Time")
            df = research["interest_over_time"]
            st.dataframe(df, use_container_width=True)
            if "date" in df.columns:
                st.line_chart(df.set_index("date"))
        for label, key in [("Top Related Queries", "related_top"), ("Rising Searches", "related_rising"), ("Regional Interest", "regional_interest")]:
            st.subheader(label)
            df = research.get(key, pd.DataFrame())
            st.dataframe(df, use_container_width=True)

with tabs[3]:
    st.header("Spotify / Music Promotion Planner")
    plan = build_spotify_music_plan(inputs)
    for k, v in plan.items():
        st.subheader(k)
        st.write(v)

    st.subheader("Playlist Submission Tracker")
    tracker = pd.DataFrame(columns=["Curator/Playlist", "Genre Fit", "Submission Date", "Status", "Result", "Notes"])
    st.data_editor(tracker, num_rows="dynamic", use_container_width=True)

with tabs[4]:
    st.header("Meta / Instagram Ads Builder")
    creative = st.session_state.get("creative", "")
    meta_plan = build_meta_plan(inputs, creative)
    st.json(meta_plan)
    st.info("Live publishing should stay paused-for-review until tracking, budget, creative, and policy checks are complete.")

with tabs[5]:
    st.header("Google / YouTube Ads Builder")
    keywords = []
    related = st.session_state.get("research", {}).get("related_top", pd.DataFrame())
    if isinstance(related, pd.DataFrame) and "query" in related.columns:
        keywords = related["query"].dropna().astype(str).head(10).tolist()
    gy_plan = build_google_youtube_plan(inputs, keywords, st.session_state.get("creative", ""))
    st.json(gy_plan)

with tabs[6]:
    st.header("Creative Studio")
    tone = st.selectbox("Creative Tone", ["luxury", "aggressive", "emotional", "viral", "professional", "streetwear", "music promo", "local business", "e-commerce"])
    if st.button("Generate Creative Pack"):
        with st.spinner("Generating creative..."):
            try:
                st.session_state["creative"] = create_creative(inputs, tone, demo_mode=(mode == "Demo Mode"))
                st.success("Creative pack generated.")
            except Exception as e:
                st.error(str(e))

    if st.session_state["creative"]:
        st.text_area("Generated Creative", value=st.session_state["creative"], height=450)

with tabs[7]:
    st.header("Campaign Development Engine")
    if st.button("Build Complete Campaign Plan"):
        meta_plan = build_meta_plan(inputs, st.session_state.get("creative", ""))
        spotify_plan = build_spotify_music_plan(inputs)
        keywords = []
        related = st.session_state.get("research", {}).get("related_top", pd.DataFrame())
        if isinstance(related, pd.DataFrame) and "query" in related.columns:
            keywords = related["query"].dropna().astype(str).head(10).tolist()
        gy_plan = build_google_youtube_plan(inputs, keywords, st.session_state.get("creative", ""))

        full_plan = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "inputs": inputs,
            "recommended_platforms": platforms,
            "budget_split": split_df.to_dict(orient="records"),
            "estimated_metrics": metrics_df.to_dict(orient="records"),
            "meta_instagram": meta_plan,
            "google_youtube": gy_plan,
            "spotify_music": spotify_plan,
            "next_actions": actions,
            "launch_checklist": [
                "Confirm tracking pixels/conversion goals.",
                "Confirm landing page loads fast on mobile.",
                "Review platform ad policies.",
                "Launch with conservative budgets first.",
                "Check results after 48–72 hours before scaling.",
            ],
        }
        st.session_state["plan_text"] = json.dumps(full_plan, indent=2)

    if st.session_state["plan_text"]:
        st.code(st.session_state["plan_text"], language="json")
        saved = save_plan_text(st.session_state["plan_text"])
        st.success(f"Saved plan to {saved}")

        csv_path = export_csv(metrics_df, "campaign_metrics.csv")
        pdf_path = export_pdf("Sullivan Marketing OS Campaign Plan", st.session_state["plan_text"], "campaign_plan.pdf")
        st.download_button("Download Metrics CSV", data=open(csv_path, "rb"), file_name="campaign_metrics.csv")
        st.download_button("Download Campaign Plan PDF", data=open(pdf_path, "rb"), file_name="campaign_plan.pdf")

with tabs[8]:
    st.header("Metrics & Optimization")
    st.write("Track performance and let the bot flag winners and losers.")
    editable = st.data_editor(metrics_df.copy(), use_container_width=True, num_rows="dynamic")
    st.caption("Metric explanations")
    st.markdown("""
- **CPC:** Cost per click. Lower is usually better, but quality matters.
- **CPM:** Cost per 1,000 impressions.
- **CTR:** Click-through rate. Shows how attractive your ad is.
- **CPA:** Cost per action or conversion.
- **ROAS:** Revenue divided by ad spend.
- **View rate:** Percent of people who watched your video ad.
- **Budget pacing:** Whether spend is too slow, on track, or burning too fast.
""")
    st.subheader("Optimization Recommendations")
    st.info("Scale platforms with strong CTR + low CPA. Cut or rewrite campaigns with weak CTR, high CPC, or no conversions after enough spend.")

with tabs[9]:
    st.header("Setup & Deployment")
    st.markdown("""
### Local setup
1. Create a folder and place these files inside it.
2. Run: `pip install -r requirements.txt`
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
4. Add your API keys.
5. Run: `streamlit run streamlit_app.py`

### Streamlit Cloud deployment
1. Push this folder to GitHub.
2. Go to Streamlit Community Cloud and deploy `streamlit_app.py`.
3. Paste your secrets into the app's **Advanced settings**.
4. Keep `.streamlit/secrets.toml` out of GitHub.

### Integration notes
- **OpenAI:** Add `OPENAI_API_KEY` for creative generation.
- **Google Trends:** Pytrends does not require an API key but can rate-limit.
- **Meta Ads:** Add Meta access token and ad account ID. Keep campaign creation paused for review.
- **Google Ads:** Add developer token, OAuth client, refresh token, and login customer ID.
- **YouTube:** Add YouTube Data API key.
- **Spotify:** Add client ID and secret for future playlist/artist data features.
""")
