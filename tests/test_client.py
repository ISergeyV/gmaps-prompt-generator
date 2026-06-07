import pytest
from models import Review, PlaceDetails
from client import GoogleMapsETL


def test_review_from_api_dict():
    raw_review = {"text": "Great service!\nHighly recommended.", "rating": 5}
    review = Review.from_api_dict(raw_review)
    assert review.text == "Great service!\nHighly recommended."
    assert review.rating == 5
    assert review.clean_snippet == "Great service! Highly recommended."


def test_review_clean_snippet_truncation():
    long_text = "a" * 250
    review = Review(text=long_text, rating=4)
    assert len(review.clean_snippet) == 203  # 200 + '...'
    assert review.clean_snippet.endswith("...")


def test_place_details_from_api_dict():
    raw_place = {
        "name": "Test Place",
        "formatted_address": "123 Test St",
        "formatted_phone_number": "555-1234",
        "rating": 4.5,
        "reviews": [
            {"text": "Bad", "rating": 2},
            {"text": "Excellent", "rating": 5},
            {"text": "Good", "rating": 4},
            {"text": "Ignore", "rating": 1},
        ],
        "editorial_summary": {"overview": "Custom overview"},
    }
    details = PlaceDetails.from_api_dict(raw_place)
    assert details.name == "Test Place"
    assert details.formatted_address == "123 Test St"
    assert details.formatted_phone_number == "555-1234"
    assert details.rating == 4.5
    assert details.overview == "Custom overview"
    # Reviews should be sorted by rating desc, and capped at 3
    assert len(details.reviews) == 3
    assert details.reviews[0].rating == 5
    assert details.reviews[1].rating == 4
    assert details.reviews[2].rating == 2


def test_place_details_from_api_dict_defaults():
    raw_place = {"name": "Simple Place"}
    details = PlaceDetails.from_api_dict(raw_place)
    assert details.name == "Simple Place"
    assert details.formatted_address == "N/A"
    assert details.formatted_phone_number == "N/A"
    assert details.rating == "N/A"
    assert details.overview == "Professional services provided locally."
    assert details.reviews == []


def test_transform_to_prompt():
    details = PlaceDetails(
        name="Mock Business",
        formatted_address="456 Rd",
        formatted_phone_number="111-222",
        rating=4.2,
        overview="Best in town.",
        reviews=[Review(text="Nice place!", rating=5)],
    )
    etl = GoogleMapsETL("AIzaMockKey")
    prompt = etl.transform_to_prompt(details)
    assert prompt is not None
    assert "Mock Business" in prompt
    assert "456 Rd" in prompt
    assert "111-222" in prompt
    assert "4.2 Stars" in prompt
    assert "Best in town." in prompt
    assert '- "Nice place!" (5/5)' in prompt


def test_extract_data_success(mocker):
    # Mock googlemaps Client
    mock_client_instance = mocker.Mock()
    mocker.patch("googlemaps.Client", return_value=mock_client_instance)

    # Mock place search and place details results
    mock_client_instance.places.return_value = {
        "results": [{"place_id": "mock_id_123", "name": "Mock Shop"}]
    }
    mock_client_instance.place.return_value = {
        "result": {
            "name": "Mock Shop",
            "formatted_address": "123 Main St",
            "formatted_phone_number": "555-5555",
            "rating": 5.0,
            "reviews": [{"text": "Love it", "rating": 5}],
            "editorial_summary": {"overview": "Great auto body work."},
        }
    }

    etl = GoogleMapsETL("AIzaMockKey")
    details = etl.extract_data("Mock Shop")

    assert details is not None
    assert details.name == "Mock Shop"
    assert details.formatted_address == "123 Main St"
    assert details.rating == 5.0
    assert len(details.reviews) == 1
    assert details.reviews[0].text == "Love it"

    # Verify API calls
    mock_client_instance.places.assert_called_once_with(query="Mock Shop")
    mock_client_instance.place.assert_called_once_with(
        place_id="mock_id_123",
        fields=[
            "name",
            "formatted_address",
            "formatted_phone_number",
            "rating",
            "reviews",
            "website",
            "opening_hours",
            "editorial_summary",
        ],
    )


def test_extract_data_no_results(mocker):
    mock_client_instance = mocker.Mock()
    mocker.patch("googlemaps.Client", return_value=mock_client_instance)

    mock_client_instance.places.return_value = {"results": []}

    etl = GoogleMapsETL("AIzaMockKey")
    details = etl.extract_data("Non-existent Business")

    assert details is None
