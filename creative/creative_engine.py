from integrations.openai_client import generate_text


def build_creative_prompt(brand, offer, audience, platform, tone, asset_type):
    return f"""
Create {asset_type} for a digital marketing campaign.

Brand/Artist: {brand}
Offer/Song/Product: {offer}
Audience: {audience}
Platform: {platform}
Tone: {tone}

Return:
1. 10 headlines
2. 10 descriptions or primary text options
3. 10 CTAs
4. 8 hooks
5. 3 short video script concepts
6. 1 campaign strategy summary
Make it practical, high-converting, and platform-ready.
""".strip()


def generate_creative_pack(api_key, brand, offer, audience, platform, tone, asset_type):
    return generate_text(api_key, build_creative_prompt(brand, offer, audience, platform, tone, asset_type))