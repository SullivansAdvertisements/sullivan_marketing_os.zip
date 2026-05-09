from integrations.openai_client import generate_marketing_copy

DEMO_CREATIVE = """HEADLINES
1. Turn Your Release Into a Real Campaign
2. Get More Fans From Every Ad Dollar
3. Launch Smarter Across Spotify, YouTube, Meta, and Google

PRIMARY TEXT
Your music deserves more than random posting. Build a focused campaign with targeted audiences, strong creative, and clear next steps.

CTAs
Listen Now • Watch Video • Join the Fan List • Book a Campaign

VIDEO HOOK
Most artists waste money because they launch without research. Here is how to build a smarter rollout.
"""

def create_creative(inputs: dict, tone: str, demo_mode: bool = True) -> str:
    if demo_mode:
        return DEMO_CREATIVE
    prompt = f"""
Create a complete ad creative pack for:
Niche: {inputs.get('niche')}
Name: {inputs.get('name')}
Offer: {inputs.get('offer')}
Goal: {inputs.get('goal')}
Audience: {inputs.get('audience')}
Location: {inputs.get('location')}
Budget: {inputs.get('budget')}

Include:
- 10 headlines
- 5 primary texts
- 5 descriptions
- 8 CTAs
- 5 video hooks
- 1 short video script
- 1 landing page hero section
- 3 social captions
- 2 email/SMS messages
"""
    return generate_marketing_copy(prompt, tone=tone)
