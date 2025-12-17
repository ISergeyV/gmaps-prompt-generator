Google Maps to LLM Prompt Generator 🗺️ ➡️ 🤖

A Python ETL (Extract, Transform, Load) utility designed for developers and agencies. It extracts structured business data (reviews, address, overview) from the Google Places API and automatically generates a detailed System Prompt.

You can feed this prompt into ChatGPT, Claude, or Gemini to instantly generate high-quality, conversion-focused landing page code.

🚀 Features

Smart Search: Finds businesses by name (no messy URLs needed).

Data Extraction: Pulls ratings, top 3 relevant reviews, and editorial summaries.

Prompt Engineering: Outputs a structured prompt optimized for Senior Developer personas.

Robust: Handles API errors and missing data gracefully.

🛠️ Installation

Clone the repo

git clone [https://github.com/YOUR_USERNAME/gmaps-prompt-generator.git](https://github.com/YOUR_USERNAME/gmaps-prompt-generator.git)
cd gmaps-prompt-generator

Set up Virtual Environment

python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Configuration
Create a .env file in the root directory:

GOOGLE_API_KEY=your_google_cloud_api_key_here

🖥️ Usage

Run the script and follow the interactive prompts:

python main.py

Example Workflow:

Enter: Google Irvine

Script fetches data...

Copy the generated prompt between the lines.

Paste into ChatGPT.

📦 Tech Stack

Python 3.10+

Google Maps API Client

Dotenv for security

📝 License

MIT
