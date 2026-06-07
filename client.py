import logging
import textwrap
from typing import Any

import googlemaps
from googlemaps.exceptions import ApiError, TransportError, Timeout

from models import PlaceDetails

logger = logging.getLogger(__name__)


class GoogleMapsETL:
    """
    ETL Engine: Handles interaction with Google API and Data Transformation.
    """

    def __init__(self, api_key: str) -> None:
        self.gmaps = googlemaps.Client(key=api_key)

    def extract_data(self, query: str) -> PlaceDetails | None:
        """
        Searches for a place by text query, retrieves its details, and returns PlaceDetails.
        """
        logger.info("Querying Google Maps API for: '%s'...", query)

        try:
            # Step 1: Search for the Place ID
            search_result = self.gmaps.places(query=query)

            if not search_result.get("results"):
                logger.warning(
                    "No results found. Try adding the city name (e.g., 'Business Name Las Vegas')."
                )
                return None

            # Step 1.1: Safe Data Extraction
            first_result = search_result["results"][0]
            place_id = first_result.get("place_id")
            place_name = first_result.get("name")

            if not place_id:
                logger.warning("Place found but no place_id was provided by the API.")
                return None

            logger.info("Found: %s (ID: %s)", place_name, place_id)

            # Step 2: Fetch Details
            details = self.gmaps.place(
                place_id=place_id,
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

            result: dict[str, Any] = details.get("result") or {}
            return PlaceDetails.from_api_dict(result)

        except ApiError as e:
            logger.error("Google Maps API error: %s", e)
            return None
        except (TransportError, Timeout) as e:
            logger.error("Connection or timeout error while contacting Google Maps API: %s", e)
            return None
        except Exception as e:
            logger.error("Unexpected error in extract_data: %s", e, exc_info=True)
            return None

    def transform_to_prompt(self, details: PlaceDetails | None) -> str | None:
        """
        Compiles the PlaceDetails into a structured Developer Prompt.
        """
        if not details:
            return None

        # Build reviews text
        reviews_text = ""
        for r in details.reviews:
            reviews_text += f'- "{r.clean_snippet}" ({r.rating}/5)\n'

        prompt_template = textwrap.dedent("""
        --- COPY BELOW THIS LINE ---

        # Role
        Act as a Senior Web Developer (HTML5/Tailwind CSS) & UX Strategist.

        # Project Context
        We are building a high-converting landing page for a real business.
        Use the data below to generate the exact content and code.

        # Business Data (Source: Google Maps)
        - **Name:** {name}
        - **Address:** {address}
        - **Phone:** {phone}
        - **Rating:** {rating} Stars
        - **Overview:** {overview}

        # Customer Testimonials (Trust Signals)
        {reviews}

        # Task Instructions
        1. **Header:** Create a compelling Hero section using the "Overview" data.
        2. **Social Proof:** Use the "Customer Testimonials" to build a reviews section.
        3. **Contact:** Ensure the address and phone are prominent in the footer/header.
        4. **Code:** Generate a **single HTML file** containing all CSS (Tailwind via CDN) and structure.

        --- END OF PROMPT ---
        """).strip()

        return prompt_template.format(
            name=details.name,
            address=details.formatted_address,
            phone=details.formatted_phone_number,
            rating=details.rating,
            overview=details.overview,
            reviews=reviews_text.strip()
        )
