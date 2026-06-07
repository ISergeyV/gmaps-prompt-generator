import logging
import sys

from client import GoogleMapsETL
from config import GOOGLE_API_KEY

# Configure logging to display info messages on stderr so they don't interfere with stdout redirection
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stderr
)

logger = logging.getLogger(__name__)


def main() -> None:
    etl = GoogleMapsETL(GOOGLE_API_KEY)

    print("=== Google Maps to Prompt Generator v1.2 (Stable) ===", file=sys.stderr)
    print("Tip: For best results, enter 'Business Name City' (e.g., 'LV Auto Body Shop Las Vegas')", file=sys.stderr)

    while True:
        try:
            # We print the prompt to stderr as well, to keep stdout clean for redirection if needed
            sys.stderr.write("\n> Enter Business Name (or 'q' to quit): ")
            sys.stderr.flush()
            user_input = sys.stdin.readline()
            if not user_input:  # EOF
                print("\nExiting...", file=sys.stderr)
                break
            user_input = user_input.strip()
        except KeyboardInterrupt:
            print("\nExiting...", file=sys.stderr)
            break

        if user_input.lower() in ["q", "quit", "exit"]:
            print("Exiting...", file=sys.stderr)
            break

        if not user_input:
            continue

        raw_data = etl.extract_data(user_input)

        if raw_data:
            final_prompt = etl.transform_to_prompt(raw_data)
            if final_prompt:
                # We print the actual generated prompt to stdout so it can be piped/redirected
                print("\n" + "=" * 40, file=sys.stderr)
                print(final_prompt)  # Goes to stdout
                print("=" * 40 + "\n", file=sys.stderr)
                print("[+] Prompt generated! Copy the text between the lines.", file=sys.stderr)


if __name__ == "__main__":
    main()
