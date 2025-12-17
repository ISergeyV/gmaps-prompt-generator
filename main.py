import os
import sys
import textwrap  # Добавлено для красивого форматирования текста
import googlemaps
from dotenv import load_dotenv

# 1. Initialization & Configuration
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

# Defensive Programming: Проверка ключа
if not API_KEY:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in .env file.")
    print("Please create a .env file with your key.")
    sys.exit(1)


class GoogleMapsETL:
    """
    ETL Engine: Handles interaction with Google API and Data Transformation.
    """

    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def extract_data(self, query):
        """
        Searches for a place by text query.
        """
        print(f"\n[*] Querying Google Maps API for: '{query}'...")

        try:
            # Step 1: Search for the Place ID
            search_result = self.gmaps.places(query=query)

            if not search_result['results']:
                print(
                    "[-] No results found. Try adding the city name (e.g., 'Business Name Las Vegas').")
                return None

            # Step 1.1: Safe Data Extraction
            first_result = search_result['results'][0]
            place_id = first_result.get('place_id')
            place_name = first_result.get('name')

            print(f"[*] Found: {place_name} (ID: {place_id})")

            # Step 2: Fetch Details
            details = self.gmaps.place(
                place_id=place_id,
                fields=['name', 'formatted_address', 'formatted_phone_number',
                        'rating', 'reviews', 'website', 'opening_hours', 'editorial_summary']
            )
            # Используем .get() на случай странного ответа API
            return details.get('result')

        except Exception as e:
            print(f"[!] API Error: {e}")
            return None

    def transform_to_prompt(self, data):
        """
        Compiles the raw JSON into a structured Developer Prompt.
        """
        if not data:
            return None

        # Обработка отзывов
        reviews_text = ""
        if 'reviews' in data:
            sorted_reviews = sorted(
                data['reviews'], key=lambda x: x.get('rating', 0), reverse=True)
            for r in sorted_reviews[:3]:
                clean_text = r.get('text', '').replace('\n', ' ')
                snippet = (
                    clean_text[:200] + '...') if len(clean_text) > 200 else clean_text
                # Защита от None в рейтинге
                rating = r.get('rating', 'N/A')
                reviews_text += f"- \"{snippet}\" ({rating}/5)\n"

        # Safe extraction for nested dictionary (Fixes the potential AttributeError)
        editorial_summary = data.get('editorial_summary') or {}
        overview_text = editorial_summary.get(
            'overview', 'Professional services provided locally.')

        # Формирование промпта без лишних отступов (dedent)
        prompt_content = f"""
        --- COPY BELOW THIS LINE ---

        # Role
        Act as a Senior Web Developer (HTML5/Tailwind CSS) & UX Strategist.

        # Project Context
        We are building a high-converting landing page for a real business.
        Use the data below to generate the exact content and code.

        # Business Data (Source: Google Maps)
        - **Name:** {data.get('name')}
        - **Address:** {data.get('formatted_address', 'N/A')}
        - **Phone:** {data.get('formatted_phone_number', 'N/A')}
        - **Rating:** {data.get('rating', 'N/A')} Stars
        - **Overview:** {overview_text}

        # Customer Testimonials (Trust Signals)
        {reviews_text}

        # Task Instructions
        1. **Header:** Create a compelling Hero section using the "Overview" data.
        2. **Social Proof:** Use the "Customer Testimonials" to build a reviews section.
        3. **Contact:** Ensure the address and phone are prominent in the footer/header.
        4. **Code:** Generate a **single HTML file** containing all CSS (Tailwind via CDN) and structure.

        --- END OF PROMPT ---
        """
        return textwrap.dedent(prompt_content)


# --- Main Runtime Loop ---
if __name__ == "__main__":
    etl = GoogleMapsETL(API_KEY)

    print("=== Google Maps to Prompt Generator v1.1 (Stable) ===")
    print("Tip: For best results, enter 'Business Name City' (e.g., 'LV Auto Body Shop Las Vegas')")

    while True:
        try:
            user_input = input(
                "\n> Enter Business Name (or 'q' to quit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if user_input.lower() in ['q', 'quit', 'exit']:
            print("Exiting...")
            break

        if not user_input:
            continue

        raw_data = etl.extract_data(user_input)

        if raw_data:
            final_prompt = etl.transform_to_prompt(raw_data)
            print("\n" + "="*40)
            print(final_prompt)
            print("="*40 + "\n")
            print("[+] Prompt generated! Copy the text between the lines.")
