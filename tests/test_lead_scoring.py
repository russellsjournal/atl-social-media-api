from backend_api.lead_scoring import calculate_lead_score
from backend_api.schemas import Business


def test_calculate_lead_score_basic():
    b = Business(
        id=1,
        name="ScoreTest",
        neighborhood=None,
        category=None,
        website="http://example.com",
        google_maps_url=None,
        has_instagram=True,
        has_facebook=True,
        reviews_count=50,
        avg_rating=4.5,
    )

    score = calculate_lead_score(b)

    expected = 10.0
    expected += 15.0  # website
    expected += 5.0   # instagram
    expected += 5.0   # facebook
    expected += min(50 * 0.2, 20.0)
    expected += 4.5 * 3

    assert score <= 100.0
    assert abs(score - expected) < 1e-6
