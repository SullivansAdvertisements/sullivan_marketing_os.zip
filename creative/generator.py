from integrations.openai_client import generate_marketing_copy

def create_creative(inputs: dict, tone: str) -> str:
    prompt = f"""
Create:
- Headlines
- Primary texts
- CTAs
- Video hooks
- Social captions
- Landing page copy

For:
Niche: {inputs.get('niche')}
Offer: {inputs.get('offer')}
Audience: {inputs.get('audience')}
Budget: {inputs.get('budget')}
"""
    return generate_marketing_copy(prompt, tone)
