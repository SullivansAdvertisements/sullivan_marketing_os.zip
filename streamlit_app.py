import base64
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Sullivan Marketing OS — Digital Marketing Beast",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

from integrations.serpapi_client import run_research, SerpApiError
from integrations.openai_client import generate_text, OpenAIClientError
from creative.creative_engine import generate_creative_pack
from campaign_builders.spotify_builder import build_spotify_plan
from campaign_builders.meta_builder import build_meta_campaign
from campaign_builders.google_builder import build_google_campaign
from campaign_builders.youtube_builder import build_youtube_campaign
from utils.metrics import allocate_budget, estimate_kpis, daily_budget
from utils.export import df_to_csv_bytes, text_to_txt_bytes, text_to_pdf_bytes


APP_TITLE = "Sullivan Marketing OS"
APP_SUBTITLE = "Digital Marketing Beast"
ASSET = Path(__file__).parent / "assets" / "sullivan_marketing_os_reference.jpeg"


def secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def image_b64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


BG64 = image_b64(ASSET)


def inject_css():
    bg_css = f"""
    background-image: linear-gradient(90deg, rgba(3,15,9,.94), rgba(3,15,9,.78)), url("data:image/jpeg;base64,{BG64}");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    """ if BG64 else "background: radial-gradient(circle at top, #24451e, #06110b 65%);"

    st.markdown(f"""
    <style>
    .stApp {{
        {bg_css}
        color: #fff3cf;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(3,18,11,.98), rgba(9,34,23,.96));
        border-right: 1px solid rgba(223,177,71,.55);
    }}
    [data-testid="stSidebar"] * {{ color: #fff3cf !important; }}
    .lux-card {{
        background: linear-gradient(145deg, rgba(5,27,18,.92), rgba(2,11,8,.88));
        border: 1px solid rgba(224,177,70,.62);
        border-radius: 22px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 0 24px rgba(220,170,50,.18), inset 0 0 22px rgba(255,216,114,.04);
        margin-bottom: 1rem;
    }}
    .hero {{
        min-height: 330px;
        border: 1px solid rgba(224,177,70,.75);
        border-radius: 28px;
        padding: 3rem 2rem;
        background:
            radial-gradient(circle at 60% 20%, rgba(240,191,70,.38), transparent 24%),
            linear-gradient(135deg, rgba(2,15,9,.68), rgba(8,36,23,.55));
        box-shadow: 0 0 42px rgba(230,180,62,.24);
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    .hero h1 {{
        color: #f6d36d;
        text-shadow: 0 0 20px rgba(245,202,94,.55);
        font-size: clamp(2.2rem, 5vw, 4.8rem);
        letter-spacing: .04em;
        margin-bottom: .1rem;
    }}
    .hero h2 {{
        color: #fff4cc;
        font-size: clamp(1.3rem, 3vw, 2.4rem);
        letter-spacing: .19em;
        margin-top: .2rem;
    }}
    .hero p {{ color: #f4d88b; letter-spacing:.14em; }}
    .metric-card {{
        background: linear-gradient(145deg, rgba(6,31,20,.95), rgba(3,14,10,.88));
        border: 1px solid rgba(230,179,67,.72);
        border-radius: 18px;
        padding: 1rem;
        min-height: 120px;
        box-shadow: 0 0 18px rgba(214,164,50,.16);
    }}
    .metric-label {{ color:#e5bd62; font-size:.86rem; }}
    .metric-value {{ color:#fff6d6; font-size:1.7rem; font-weight:800; }}
    .metric-help {{ color:#b9d58f; font-size:.78rem; }}
    .gold-title {{ color:#f2ca67; letter-spacing:.06em; text-transform:uppercase; }}
    .stButton>button, .stDownloadButton>button {{
        background: linear-gradient(180deg, #f3ce72, #a86e18);
        color: #101409 !important;
        border: 1px solid #ffdf82;
        border-radius: 12px;
        font-weight: 800;
    }}
    div[data-baseweb="tab-list"] button {{
        color: #fff3cf;
        border-radius: 12px 12px 0 0;
    }}
    div[data-baseweb="tab-list"] button[aria-selected="true"] {{
        background: rgba(221,172,57,.20);
        color: #ffe08a;
    }}
    .small-note {{ color:#d9c58b; font-size:.9rem; }}
    </style>
    """, unsafe_allow_html=True)


inject_css()


def money(x):
    return f"${x:,.2f}"


def kpi_card(label, value, help_text=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-help">{help_text}</div>
    </div>
    """, unsafe_allow_html=True)


@st.cache_data(show_spinner=False, ttl=3600)
def cached_serpapi(api_key, query, country, timeframe, platform_focus, search_type):
    return run_research(api_key, query, country, timeframe, platform_focus, search_type)


def sidebar_inputs():
    with st.sidebar:
        st.markdown("## 👑 Sullivan’s Innovative")
        st.markdown("### MARKETING OS")
        st.divider()
        live_default = True
        demo_mode = st.toggle("Demo mode", value=False, help="Live mode is default. Demo mode uses sample outputs only when you turn this on.")
        st.caption("Live mode uses SerpApi and OpenAI keys from Streamlit secrets.")
        st.divider()
        brand = st.text_input("Brand / artist name", "Sullivan’s Innovative")
        offer = st.text_input("Offer / song / product", "Premium music marketing campaign")
        goal = st.selectbox("Campaign goal", ["Awareness", "Engagement", "Traffic", "Leads", "Sales", "Video views", "Music promotion", "Clothing brand promotion", "E-commerce"])
        budget = st.number_input("Total budget", min_value=100.0, value=15000.0, step=100.0)
        timeframe_days = st.number_input("Timeframe days", min_value=1, value=30, step=1)
        locations = st.text_input("Target locations", "United States, Canada, United Kingdom")
        audience = st.text_area("Audience", "Fans of hip-hop, streetwear, music videos, YouTube content, and premium brands")
        platforms = st.multiselect(
            "Platforms",
            ["Spotify", "Meta / Instagram", "Google Ads", "YouTube Ads", "Research & Tools"],
            default=["Spotify", "Meta / Instagram", "Google Ads", "YouTube Ads", "Research & Tools"],
        )
        return {
            "demo_mode": demo_mode,
            "brand": brand,
            "offer": offer,
            "goal": goal,
            "budget": budget,
            "timeframe_days": int(timeframe_days),
            "locations": locations,
            "audience": audience,
            "platforms": platforms,
        }


S = sidebar_inputs()
SERPAPI_API_KEY = secret("SERPAPI_API_KEY")
OPENAI_API_KEY = secret("OPENAI_API_KEY")

alloc = allocate_budget(S["budget"], S["platforms"])
kpis = estimate_kpis(S["budget"], S["goal"])

st.markdown(f"""
<div class="hero">
    <h1>{APP_TITLE}</h1>
    <h2>{APP_SUBTITLE}</h2>
    <p>THE ULTIMATE DIGITAL MARKETING BEAST</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "🏠 Dashboard",
    "🧠 Strategy Builder",
    "🔎 SerpApi Research Center",
    "🎵 Spotify Planner",
    "📱 Meta / Instagram Ads",
    "🔍 Google Ads",
    "▶️ YouTube Ads",
    "✨ OpenAI Creative Studio",
    "👑 Campaign Development Engine",
    "📤 Export Center",
])


with tabs[0]:
    st.markdown('<h3 class="gold-title">Campaign Overview</h3>', unsafe_allow_html=True)
    c = st.columns(5)
    with c[0]: kpi_card("Total Budget", money(S["budget"]), "Campaign budget")
    with c[1]: kpi_card("Est. Reach", f"{kpis['Estimated Reach']:,}", "People reached")
    with c[2]: kpi_card("Est. Clicks", f"{kpis['Estimated Clicks']:,}", "Traffic estimate")
    with c[3]: kpi_card("Est. Views", f"{kpis['Estimated Views']:,}", "Video/view estimate")
    with c[4]: kpi_card("Health Score", f"{kpis['Campaign Health Score']}/100", "Planning quality")

    st.markdown('<div class="lux-card">', unsafe_allow_html=True)
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Budget Allocation")
        if alloc:
            alloc_df = pd.DataFrame({"Platform": list(alloc.keys()), "Budget": list(alloc.values())})
            fig = px.pie(alloc_df, names="Platform", values="Budget", hole=.55)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#fff3cf")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(alloc_df, use_container_width=True)
    with right:
        st.subheader("Performance Overview")
        perf = pd.DataFrame({
            "Day": list(range(1, 31)),
            "Reach": [int(kpis["Estimated Reach"] * (i / 30) ** 1.1) for i in range(1, 31)],
            "Clicks": [int(kpis["Estimated Clicks"] * (i / 30) ** 1.05) for i in range(1, 31)],
            "Conversions": [int(kpis["Estimated Leads/Conversions"] * (i / 30) ** 1.15) for i in range(1, 31)],
        })
        fig = px.line(perf, x="Day", y=["Reach", "Clicks", "Conversions"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#fff3cf")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c2 = st.columns(5)
    metric_pairs = [
        ("CPC", f"${kpis['CPC']}", "Avg click cost"),
        ("CPM", f"${kpis['CPM']}", "Cost per 1,000 impressions"),
        ("CTR", f"{kpis['CTR']}%", "Click-through rate"),
        ("CPA", f"${kpis['CPA']}", "Cost per acquisition"),
        ("ROAS", f"{kpis['ROAS']}x", "Return on ad spend"),
    ]
    for col, pair in zip(c2, metric_pairs):
        with col:
            kpi_card(*pair)

    c3 = st.columns(5)
    more_pairs = [
        ("Cost Per View", f"${kpis['Cost Per View']}", "Video view cost"),
        ("Streams", f"{kpis['Estimated Streams']:,}", "Spotify/music estimate"),
        ("Saves", f"{kpis['Estimated Saves']:,}", "Estimated saves"),
        ("Followers", f"{kpis['Estimated Followers']:,}", "Growth estimate"),
        ("Engagement Rate", f"{kpis['Engagement Rate']}%", "Engagement target"),
    ]
    for col, pair in zip(c3, more_pairs):
        with col:
            kpi_card(*pair)

    st.markdown('<div class="lux-card">', unsafe_allow_html=True)
    st.subheader("Recommended Next Actions")
    st.write("- Increase budget toward the lowest-cost winning platform after 72 hours of data.")
    st.write("- Test 3 hooks per platform before judging campaign performance.")
    st.write("- Separate cold audiences from retargeting audiences.")
    st.write("- Use SerpApi research to refresh keyword, competitor, and topic angles weekly.")
    st.write("- Scale in 20–30% budget jumps when KPIs stay stable.")
    st.markdown('</div>', unsafe_allow_html=True)


with tabs[1]:
    st.markdown('<h3 class="gold-title">Strategy Builder</h3>', unsafe_allow_html=True)
    st.markdown('<div class="lux-card">', unsafe_allow_html=True)
    st.write(f"**Brand/Artist:** {S['brand']}")
    st.write(f"**Goal:** {S['goal']}")
    st.write(f"**Daily Budget:** {money(daily_budget(S['budget'], S['timeframe_days']))}")
    st.write("**Recommended Platform Mix**")
    st.dataframe(pd.DataFrame({"Platform": list(alloc.keys()), "Budget": list(alloc.values())}), use_container_width=True)
    st.write("**Campaign Funnel:** Awareness → Engagement → Traffic/View → Retargeting → Conversion/Follow/Stream.")
    st.write("**Audience Strategy:** Start broad enough for platform learning, then segment by engager, viewer, visitor, buyer, and playlist listener behavior.")
    st.write("**Creative Direction:** Premium gold/green brand visuals, fast hooks, proof-based copy, strong offer clarity, and platform-specific short-form variants.")
    st.write("**Launch Checklist:** tracking, pixels, UTMs, budgets, locations, negative keywords, creative sizes, landing page, compliance review.")
    st.write("**Optimization Checklist:** cut weak creatives, move budget to winners, expand high-intent keywords, retarget warm users, refresh hooks weekly.")
    st.markdown('</div>', unsafe_allow_html=True)


with tabs[2]:
    st.markdown('<h3 class="gold-title">SerpApi Research Center</h3>', unsafe_allow_html=True)
    st.caption("Live mode uses SerpApi. No pytrends is imported or used.")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        rq = st.text_input("Keyword / artist / brand / niche", S["offer"])
        country = st.text_input("Country code", "US")
    with col_b:
        timeframe = st.selectbox("Google Trends timeframe", ["now 7-d", "today 1-m", "today 3-m", "today 12-m", "today 5-y"], index=3)
        platform_focus = st.selectbox("Platform focus", ["Google", "YouTube", "music", "e-commerce", "local business", "streetwear", "general"])
    with col_c:
        search_type = st.selectbox("Search type", ["trends", "search results", "related searches", "competitor research", "keyword ideas", "audience intent", "content angle research", "music/video topic research"])

    if st.button("Launch Live Research", key="research_btn"):
        if S["demo_mode"]:
            st.warning("Demo mode is on. Turn it off for real SerpApi data.")
            demo_df = pd.DataFrame({"Topic": ["premium music marketing", "youtube ads for artists", "spotify playlist pitching"], "Intent": ["Research", "Promotion", "Growth"]})
            st.dataframe(demo_df, use_container_width=True)
            st.session_state["last_research_df"] = demo_df
        else:
            try:
                with st.spinner("Running SerpApi live research..."):
                    research = cached_serpapi(SERPAPI_API_KEY, rq, country, timeframe, platform_focus, search_type)
                st.success(research.get("summary", "Research complete."))
                if "trend_df" in research and not research["trend_df"].empty:
                    st.subheader("Keyword Trend Summary")
                    st.dataframe(research["trend_df"], use_container_width=True)
                    fig = px.line(research["trend_df"], x="date", y="interest", color="keyword")
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#fff3cf")
                    st.plotly_chart(fig, use_container_width=True)
                    st.session_state["last_research_df"] = research["trend_df"]
                if "results_df" in research and not research["results_df"].empty:
                    st.subheader("Search Result Snippets")
                    st.dataframe(research["results_df"], use_container_width=True)
                    st.session_state["last_research_df"] = research["results_df"]
                if research.get("related_searches"):
                    st.subheader("Related / Rising Topics")
                    st.write(research["related_searches"])
                if "region_df" in research and not research["region_df"].empty:
                    st.subheader("Regional Interest")
                    st.dataframe(research["region_df"], use_container_width=True)
                if not any([
                    ("trend_df" in research and not research["trend_df"].empty),
                    ("results_df" in research and not research["results_df"].empty),
                    research.get("related_searches"),
                ]):
                    st.info("SerpApi returned limited data for this query. Try a broader keyword, different country, or a different search type.")
            except SerpApiError as e:
                st.error(str(e))
                st.info("Check that SERPAPI_API_KEY is set in Streamlit secrets, your SerpApi account has credits, and the selected engine/search type is supported.")
            except Exception as e:
                st.error(f"Unexpected research error: {e}")


with tabs[3]:
    st.markdown('<h3 class="gold-title">Spotify / Music Promotion Planner</h3>', unsafe_allow_html=True)
    genre = st.text_input("Genre", "Hip-hop / Rap")
    plan = build_spotify_plan(S["brand"], S["offer"], genre, alloc.get("Spotify", S["budget"] * .2), S["locations"])
    for k, v in plan.items():
        st.markdown(f"**{k}**")
        st.write(v)
    tracker = pd.DataFrame(columns=["Playlist", "Contact", "Genre", "Submitted Date", "Status", "Placement", "Estimated Streams"])
    st.download_button("Download Playlist Tracker CSV", df_to_csv_bytes(tracker), "playlist_submission_tracker.csv", "text/csv")


with tabs[4]:
    st.markdown('<h3 class="gold-title">Meta / Instagram Ads Builder</h3>', unsafe_allow_html=True)
    meta = build_meta_campaign(S["brand"], S["offer"], S["goal"], alloc.get("Meta / Instagram", S["budget"] * .25), S["audience"])
    for k, v in meta.items():
        st.markdown(f"**{k}**")
        st.write(v)
    if not secret("META_ACCESS_TOKEN"):
        st.info("META_ACCESS_TOKEN is optional. This builder still works without it, but live publishing would require Meta API setup.")


with tabs[5]:
    st.markdown('<h3 class="gold-title">Google Ads Builder</h3>', unsafe_allow_html=True)
    google = build_google_campaign(S["brand"], S["offer"], S["goal"], alloc.get("Google Ads", S["budget"] * .25), S["locations"])
    for k, v in google.items():
        st.markdown(f"**{k}**")
        st.write(v)
    if not secret("GOOGLE_ADS_DEVELOPER_TOKEN"):
        st.info("GOOGLE_ADS_DEVELOPER_TOKEN is optional. Planning works now; live campaign creation requires Google Ads API credentials.")


with tabs[6]:
    st.markdown('<h3 class="gold-title">YouTube Ads Builder</h3>', unsafe_allow_html=True)
    yt = build_youtube_campaign(S["brand"], S["offer"], S["goal"], alloc.get("YouTube Ads", S["budget"] * .22), S["audience"])
    for k, v in yt.items():
        st.markdown(f"**{k}**")
        st.write(v)
    if not secret("YOUTUBE_API_KEY"):
        st.info("YOUTUBE_API_KEY is optional. SerpApi YouTube search can still support research when your SerpApi key is active.")


with tabs[7]:
    st.markdown('<h3 class="gold-title">OpenAI Creative Studio</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        platform = st.selectbox("Creative platform", ["Meta / Instagram", "Google Ads", "YouTube Ads", "Spotify", "Landing Page", "Email", "SMS"])
    with c2:
        tone = st.selectbox("Tone", ["Luxury", "Aggressive", "Viral", "Emotional", "Professional", "Streetwear", "Music promo", "Local business", "E-commerce", "High-ticket"])
    with c3:
        asset_type = st.selectbox("Asset type", ["Full campaign pack", "Headlines", "Descriptions", "CTAs", "Hooks", "Video scripts", "Landing page copy", "Social captions", "Email copy", "SMS copy"])
    if st.button("Generate Creative Pack"):
        if S["demo_mode"]:
            output = f"DEMO CREATIVE PACK for {S['brand']} — {S['offer']}\n\nHeadlines:\n1. Built Different. Seen Everywhere.\n2. Premium Campaigns. Real Momentum.\n\nHooks:\n1. Stop scrolling — this is the move.\n2. Your next audience is already waiting."
            st.session_state["last_copy"] = output
            st.text_area("Creative Output", output, height=360)
        else:
            try:
                with st.spinner("Generating with OpenAI..."):
                    output = generate_creative_pack(OPENAI_API_KEY, S["brand"], S["offer"], S["audience"], platform, tone, asset_type)
                st.session_state["last_copy"] = output
                st.text_area("Creative Output", output, height=520)
            except OpenAIClientError as e:
                st.error(str(e))
                st.info("Check OPENAI_API_KEY in Streamlit secrets and confirm your OpenAI billing/quota is active.")


with tabs[8]:
    st.markdown('<h3 class="gold-title">Campaign Development Engine — Beast Mode</h3>', unsafe_allow_html=True)
    st.write("Combines your inputs, SerpApi research, OpenAI creative, platform rules, budget logic, and KPI targets.")
    if st.button("Build Complete Beast Mode Campaign"):
        research_context = ""
        if "last_research_df" in st.session_state:
            research_context = st.session_state["last_research_df"].head(10).to_string(index=False)
        prompt = f"""
Build a complete platform-by-platform digital marketing campaign.

Brand/Artist: {S['brand']}
Offer/Song/Product: {S['offer']}
Goal: {S['goal']}
Budget: {S['budget']}
Timeframe days: {S['timeframe_days']}
Locations: {S['locations']}
Audience: {S['audience']}
Platforms: {S['platforms']}
Budget split: {alloc}
KPI targets: {kpis}
Recent SerpApi research table:
{research_context}

Return:
1. Campaign plan
2. Platform-by-platform launch plan
3. Budget split
4. Audience targeting
5. Keywords
6. Negative keywords
7. Ad copy
8. Video hooks
9. Playlist strategy
10. KPI goals
11. Daily optimization checklist
12. 7-day, 14-day, and 30-day scaling plan
13. Export-ready table format
"""
        if S["demo_mode"]:
            output = f"""BEAST MODE DEMO PLAN

Campaign: {S['brand']} — {S['offer']}
Budget Split: {alloc}

7-Day Plan: launch tests, collect data, cut weak hooks.
14-Day Plan: scale winning ad sets by 20-30%.
30-Day Plan: build retargeting, refresh creative, expand best markets.

Use live mode with SerpApi + OpenAI for full custom output."""
        else:
            try:
                with st.spinner("Building Beast Mode campaign..."):
                    output = generate_text(OPENAI_API_KEY, prompt)
            except OpenAIClientError as e:
                st.error(str(e))
                output = ""
        if output:
            st.session_state["campaign_plan"] = output
            st.text_area("Complete Campaign Plan", output, height=620)


with tabs[9]:
    st.markdown('<h3 class="gold-title">Export Center</h3>', unsafe_allow_html=True)
    summary = f"""
{APP_TITLE} — {APP_SUBTITLE}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Brand/Artist: {S['brand']}
Offer/Song/Product: {S['offer']}
Goal: {S['goal']}
Budget: {money(S['budget'])}
Timeframe: {S['timeframe_days']} days
Locations: {S['locations']}
Audience: {S['audience']}
Platforms: {', '.join(S['platforms'])}

Budget Split:
{pd.DataFrame({"Platform": list(alloc.keys()), "Budget": list(alloc.values())}).to_string(index=False)}

KPI Targets:
{pd.DataFrame({"Metric": list(kpis.keys()), "Value": list(kpis.values())}).to_string(index=False)}

Campaign Plan:
{st.session_state.get("campaign_plan", "No Beast Mode campaign generated yet.")}
"""
    plan_df = pd.DataFrame({"Platform": list(alloc.keys()), "Budget": list(alloc.values())})
    kpi_df = pd.DataFrame({"Metric": list(kpis.keys()), "Value": list(kpis.values())})
    copy_text = st.session_state.get("last_copy", "No copywriting pack generated yet.")
    research_df = st.session_state.get("last_research_df", pd.DataFrame({"Message": ["No research exported yet. Run SerpApi Research Center first."]}))

    st.download_button("Download Campaign Plan CSV", df_to_csv_bytes(plan_df), "campaign_budget_plan.csv", "text/csv")
    st.download_button("Download KPI Targets CSV", df_to_csv_bytes(kpi_df), "campaign_kpi_targets.csv", "text/csv")
    st.download_button("Download Research Results CSV", df_to_csv_bytes(research_df), "serpapi_research_results.csv", "text/csv")
    st.download_button("Download Copywriting Pack TXT", text_to_txt_bytes(copy_text), "copywriting_pack.txt", "text/plain")
    st.download_button("Download Campaign Summary TXT", text_to_txt_bytes(summary), "campaign_summary.txt", "text/plain")
    st.download_button("Download Campaign Summary PDF", text_to_pdf_bytes("Sullivan Marketing OS Campaign Summary", summary), "campaign_summary.pdf", "application/pdf")

st.markdown("""
<div class="lux-card" style="text-align:center;">
    <h3 class="gold-title">Sullivan’s Innovative Marketing OS</h3>
    <p class="small-note">Built for visionaries. Designed to dominate.</p>
</div>
""", unsafe_allow_html=True)