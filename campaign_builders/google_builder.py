def build_google_campaign(brand, offer, goal, budget, locations):
    seed = str(offer).lower()
    return {
        "Campaign Structure": ["Brand search", "High-intent non-brand search", "Competitor conquest", "Retargeting display/video"],
        "Keyword Groups": [
            [seed, f"best {seed}", f"{seed} near me", f"buy {seed}"],
            [f"{brand} {seed}", f"{brand} official", f"{brand} promo"],
        ],
        "Negative Keywords": ["free", "torrent", "jobs", "salary", "meaning", "template", "scam"],
        "Headlines": [f"{brand} Official", f"Get {offer}", "Premium Quality", "Limited Campaign"],
        "Descriptions": [f"Discover {offer} from {brand}. Built for people ready to take action.", "Start today with a focused campaign and clear next steps."],
        "Sitelinks": ["Pricing", "Book a Call", "Latest Work", "Contact"],
        "Callouts": ["Fast Launch", "Premium Creative", "Real Results", "Clear Reporting"],
        "Bidding": "Start with Maximize Clicks or Maximize Conversions once conversion tracking is verified.",
        "Locations": locations,
        "Budget Pacing": f"${float(budget):,.2f} total. Protect 20-30% for winning keyword scale-up."
    }