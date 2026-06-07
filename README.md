# Google Maps to LLM Prompt Generator 🗺️ ➡️ 🤖

A modern, modular Python ETL (Extract, Transform, Load) utility designed for developers and agencies. It extracts structured business data (reviews, address, overview) from the Google Places API and automatically generates a detailed System Prompt.

You can feed this prompt into ChatGPT, Claude, or Gemini to instantly generate high-quality, conversion-focused landing page code.

---

## 🚀 Features

* **Smart Search:** Finds businesses by name (no messy Google Maps URLs needed).
* **Robust Data ETL:** Pulls ratings, top 3 relevant reviews (sorted by rating descending), and editorial summaries using strongly-typed models.
* **Separation of Concerns:** Clean architecture separating API interaction, data modeling, environment configuration, and user CLI logic.
* **Stdout/Stderr Splitting:** Standard logs and interactive inputs are written to `sys.stderr`, allowing you to pipe the output prompt directly to a file (e.g., `python main.py > prompt.txt`).
* **Test Suite:** Mocked unit tests verifying data models and API interactions without spending live API quotas.

---

## 🛠️ Architecture

The project has been refactored into a structured, modular codebase:
* **[config.py](file:///home/isv/desktop/projects/gmaps-prompt-generator/config.py):** Environment variables loading and validation.
* **[models.py](file:///home/isv/desktop/projects/gmaps-prompt-generator/models.py):** Typed data structures (`Review` and `PlaceDetails`).
* **[client.py](file:///home/isv/desktop/projects/gmaps-prompt-generator/client.py):** ETL Client with explicit error handling and prompt templates.
* **[main.py](file:///home/isv/desktop/projects/gmaps-prompt-generator/main.py):** Interactive CLI loop and standard output routing.
* **[pyproject.toml](file:///home/isv/desktop/projects/gmaps-prompt-generator/pyproject.toml):** Modern PEP 621 packaging metadata and tool configs.

---

## 💻 Installation

### 1. Set up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
Install the package in editable mode along with development tools:
```bash
pip install -e .
pip install pytest pytest-mock ruff
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_cloud_api_key_here
```

---

## 🖥️ Usage

Run the script and follow the interactive prompts:
```bash
python main.py
```

To output the prompt directly into a file (useful for LLM workflows):
```bash
python main.py > output_prompt.txt
```

---

## 🧪 Testing and Quality Control

### Running Tests
Execute the unit test suite:
```bash
pytest tests/
```

### Linting
Check code style with `ruff`:
```bash
ruff check .
```

---

## 📦 Tech Stack

* Python 3.10+
* Google Maps API Client for Python
* pytest & pytest-mock
* python-dotenv
* ruff

---

## 📝 License

MIT
