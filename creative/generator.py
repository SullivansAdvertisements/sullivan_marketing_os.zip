from integrations.openai_client import generate_marketing_copy

DEMO_CREATIVE = """LUXURY CREATIVE PACK

HEADLINES
1. Turn Your Campaign Into a Premium Growth Machine
2. Launch Smarter Across Spotify, Meta, Google, and YouTube
3. Stop Guessing. Build a Data-Driven Campaign.

PRIMARY TEXT
Sullivan’s Innovative Marketing OS helps turn your brand, song, or offer into a complete launch plan with research, targeting, creative, and next steps.

CTAs
Launch My Campaign • Build My Strategy • Grow My Audience • Start the Rollout

VIDEO HOOK
Most campaigns fail because they launch without research. This system helps you build the plan before you burn the budget.
"""

def create_creative(inputs: dict, tone: str, demo_mode: bool = True) -> str:
    if demo_mode:
        return DEMO_CREATIVE
    prompt = f"""
Create a full premium ad creative pack for:
Niche: {inputs.get('niche')}
Name: {inputs.get('name')}
Offer: {inputs.get('offer')}
Goal: {inputs.get('goal')}
Audience: {inputs.get('audience')}
Location: {inputs.get('location')}
Budget: {inputs.get('budget')}

Include 10 headlines, 5 primary texts, 5 descriptions, 8 CTAs, 5 video hooks,
1 video script, landing page hero copy, 3 social captions, and 2 email/SMS messages.
"""
    return generate_marketing_copy(prompt, tone=tone)
