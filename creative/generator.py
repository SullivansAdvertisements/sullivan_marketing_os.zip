from integrations.openai_client import generate_marketing_copy

def create_creative(inputs: dict, tone: str) -> str:
    prompt = f"""
Create a full premium ad creative pack for:
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
- 2 email/SMS campaign messages
"""
    return generate_marketing_copy(prompt, tone=tone)
