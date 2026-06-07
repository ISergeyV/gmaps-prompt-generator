from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Review:
    text: str
    rating: float | str = "N/A"

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> "Review":
        return cls(
            text=data.get("text", ""),
            rating=data.get("rating", "N/A")
        )

    @property
    def clean_snippet(self) -> str:
        clean_text = self.text.replace("\n", " ").strip()
        if len(clean_text) > 200:
            return clean_text[:200] + "..."
        return clean_text


@dataclass(frozen=True)
class PlaceDetails:
    name: str
    formatted_address: str = "N/A"
    formatted_phone_number: str = "N/A"
    rating: float | str = "N/A"
    overview: str = "Professional services provided locally."
    reviews: list[Review] = field(default_factory=list)

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> "PlaceDetails":
        raw_reviews = data.get("reviews", [])
        # Sort reviews by rating descending, mapping None/missing rating to 0 for sorting
        sorted_raw_reviews = sorted(
            raw_reviews,
            key=lambda x: x.get("rating") if x.get("rating") is not None else 0,
            reverse=True
        )
        reviews = [Review.from_api_dict(r) for r in sorted_raw_reviews[:3]]

        editorial_summary = data.get("editorial_summary") or {}
        overview = editorial_summary.get("overview") or "Professional services provided locally."

        return cls(
            name=data.get("name", "Unknown Business"),
            formatted_address=data.get("formatted_address", "N/A"),
            formatted_phone_number=data.get("formatted_phone_number", "N/A"),
            rating=data.get("rating", "N/A"),
            overview=overview,
            reviews=reviews
        )
