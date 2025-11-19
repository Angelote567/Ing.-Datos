# tab_processor/results/main.py

import os
import click

# Base directory for all generated files
BASE_DIR = "./files"

# We define the main output directories we want to check
OUTPUT_DIRS = {
    "raw_songs": os.path.join(BASE_DIR, "songs"),                    # scrapper output
    "cleaned_songs": os.path.join(BASE_DIR, "cleaned"),              # cleaner output
    "validator_ok": os.path.join(BASE_DIR, "validations", "ok"),     # valid tabs
    "validator_ko": os.path.join(BASE_DIR, "validations", "ko"),     # invalid tabs
}

def count_files(path: str) -> int:
    """
    Count how many files we have in a directory (recursively).
    Only counts regular files, not folders.
    """
    total_files = 0
    for root, _, files in os.walk(path):
        total_files += len(files)
    return total_files

@click.command()
def main():
    """Print a small summary of how many files we have for each output."""
    print("=== Results summary ===")
    for name, path in OUTPUT_DIRS.items():
        if os.path.exists(path):
            num_files = count_files(path)
            print(f"{name}: {num_files} files ({path})")
        else:
            print(f"{name}: directory not found ({path})")

if __name__ == "__main__":
    main()
