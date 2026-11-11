"""Command line interface."""
import argparse
import json
from .analyzer import analyze_file


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenDevKit AI — local-first Python code analyzer")
    parser.add_argument("file", help="Path to a Python source file")
    args = parser.parse_args()
    try:
        print(json.dumps(analyze_file(args.file), indent=2))
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")

if __name__ == "__main__":
    main()
