from .schemas import Business

def calculate_lead_score(business: Business) -> float:
    score = 10.0

    if business.website:
        score += 15.0
    if business.has_instagram:
        score += 5.0
    if business.has_facebook:
        score += 5.0

    score += min(business.reviews_count * 0.2, 20.0)
    score += business.avg_rating * 3

    return min(score, 100.0)
