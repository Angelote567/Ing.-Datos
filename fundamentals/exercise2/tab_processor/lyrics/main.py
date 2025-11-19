import os
import re
import click

BASE_DIR = "./files"
OK_DIR = os.path.join(BASE_DIR, "validations", "ok")


def list_txt_files_recursive(path: str):
    """Return all .txt files under a directory (recursively)."""
    txt_files = []
    for root, _, files in os.walk(path):
        for name in files:
            if name.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, name))
    return txt_files


def remove_chords_from_line(line: str) -> str:
    """
    Remove chord tokens from a line.

    Chords are patterns like:
    A, Am, A#, Bb, Fmaj7, Gm7, etc.
    """
    # Pattern for common chord formats (uppercase letters)
    chord_pattern = r"\b([A-G](?:#|b)?(?:maj|min|m|sus|dim|aug)?\d*)\b"

    # Remove chords
    without_chords = re.sub(chord_pattern, "", line)

    # Remove leftover double spaces
    without_chords = re.sub(r"\s{2,}", " ", without_chords)

    # Strip spaces at start/end
    return without_chords.strip()


def process_file(input_path: str) -> str:
    """Read a file and return its content without chords."""
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Remove newline for processing
        text = line.rstrip("\n")
        new_text = remove_chords_from_line(text)

        # Keep empty lines to preserve structure
        cleaned_lines.append(new_text)

    # Join back with newline
    return "\n".join(cleaned_lines)


@click.command()
def main():
    """
    Generate lyrics-only versions of validated tabs.

    For each file in ./files/validations/ok,
    create a new file <name>_lyrics.txt in the same directory.
    """
    if not os.path.exists(OK_DIR):
        print(f"Directory not found: {OK_DIR}")
        return

    files = list_txt_files_recursive(OK_DIR)
    print(f"Found {len(files)} validated files to process.\n")

    count = 0
    for path in files:
        dir_name, filename = os.path.split(path)
        name, ext = os.path.splitext(filename)

        # Output file: same directory, *_lyrics.txt
        output_path = os.path.join(dir_name, f"{name}_lyrics{ext}")

        lyrics_text = process_file(path)

        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(lyrics_text + "\n")

        count += 1
        print(f"[{count}] {output_path} CREATED")

    print("\nLyrics generation finished.")
    print(f"Total files processed: {count}")


if __name__ == "__main__":
    main()
