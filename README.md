# Sullivan Marketing OS — Digital Marketing Beast

A polished Streamlit dashboard for music promotion, Meta/Instagram Ads, Google/YouTube Ads, Google Trends research, OpenAI-powered creative generation, campaign planning, and optimization.

## Main features
- Dashboard with budget split, estimated metrics, health score, and next actions
- Strategy Builder for low-budget and growth campaigns
- Research Center using Google Trends/pytrends
- Spotify/Music Promotion Planner
- Meta/Instagram Ads Builder
- Google/YouTube Ads Builder
- Creative Studio powered by OpenAI
- Campaign Development Engine with export to CSV/PDF
- Metrics & Optimization dashboard

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Secrets
Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` locally. Never commit real secrets.

## Deploy
Push to GitHub, deploy `streamlit_app.py` on Streamlit Community Cloud, and paste secrets into Advanced settings.
