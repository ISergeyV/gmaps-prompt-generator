import os
import sys
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in .env file.", file=sys.stderr)
    print("Please create a .env file with your key.", file=sys.stderr)
    sys.exit(1)
