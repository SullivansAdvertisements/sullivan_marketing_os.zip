# Sullivan Marketing OS — Digital Marketing Beast

A production-ready Streamlit digital marketing bot for campaign planning, SerpApi research, Spotify/music promotion planning, Meta/Instagram Ads planning, Google Ads planning, YouTube Ads planning, OpenAI creative generation, KPI forecasting, and exports.

## What this app includes

- Dashboard with budget allocation, reach, clicks, views, conversions, streams, saves, followers, CPC, CPM, CTR, CPA, ROAS, cost per view, and engagement rate
- Strategy Builder
- SerpApi Research Center
- Spotify / Music Promotion Planner
- Meta / Instagram Ads Builder
- Google Ads Builder
- YouTube Ads Builder
- OpenAI Creative Studio
- Campaign Development Engine
- Export Center with CSV, TXT, and PDF downloads
- Luxury Sullivan’s Innovative green/gold interface inspired by the supplied reference image

## SerpApi replaces Google Trends / pytrends

This app does **not** use pytrends and does **not** import pytrends anywhere.

Instead, Google Trends and research are handled through SerpApi using `requests`.

SerpApi is used for:

- Google Trends research with `engine=google_trends`
- Google Search research with `engine=google`
- YouTube Search research with `engine=youtube`
- Related searches
- Rising topics when returned
- Regional trend data when returned
- Competitor research
- Keyword ideas
- Audience intent research
- Music/video topic research

The SerpApi integration is located here:

```text
integrations/serpapi_client.py
```

## Required files

```text
streamlit_app.py
requirements.txt
.streamlit/config.toml
.streamlit/secrets.toml.example
integrations/serpapi_client.py
integrations/openai_client.py
campaign_builders/meta_builder.py
campaign_builders/google_builder.py
campaign_builders/youtube_builder.py
campaign_builders/spotify_builder.py
creative/creative_engine.py
utils/metrics.py
utils/export.py
assets/sullivan_marketing_os_reference.jpeg
README.md
```

## Local setup

1. Install Python 3.10, 3.11, or 3.12.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create Streamlit secrets:

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

4. Add your real keys to `.streamlit/secrets.toml`:

```toml
SERPAPI_API_KEY = "your_serpapi_key"
OPENAI_API_KEY = "your_openai_key"

META_ACCESS_TOKEN = ""
GOOGLE_ADS_DEVELOPER_TOKEN = ""
YOUTUBE_API_KEY = ""
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
```

5. Run the app:

```bash
streamlit run streamlit_app.py
```

## Streamlit Cloud deployment

1. Upload this folder to a GitHub repository.
2. In Streamlit Cloud, create a new app.
3. Choose the repo.
4. Set the main file path to:

```text
streamlit_app.py
```

5. Add secrets in Streamlit Cloud:

```toml
SERPAPI_API_KEY = "your_serpapi_key"
OPENAI_API_KEY = "your_openai_key"

META_ACCESS_TOKEN = ""
GOOGLE_ADS_DEVELOPER_TOKEN = ""
YOUTUBE_API_KEY = ""
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
```

6. Deploy.

## Important notes

- Live mode is the default.
- Demo mode is only used when the user turns on the demo toggle.
- If SerpApi fails, the app shows a user-friendly error and tells the user what to check.
- Optional ad platform keys are not required for the builders to work.
- The app is campaign-planning ready. Direct ad publishing requires deeper OAuth approval and production API setup for each ad platform.