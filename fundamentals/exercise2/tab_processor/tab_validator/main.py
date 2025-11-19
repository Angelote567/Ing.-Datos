# Importamos las bibliotecas necesarias
import os
import click
import re
import logging as log
import datetime
import shutil

## CHANGED: use cleaned/ok/ko directories built with os.path.join
INPUT_DIRECTORY = "./files/"
CLEANED_DIRECTORY = os.path.join(INPUT_DIRECTORY, "cleaned")
OUTPUT_DIRECTORY_OK = os.path.join(INPUT_DIRECTORY, "validations", "ok")
OUTPUT_DIRECTORY_KO = os.path.join(INPUT_DIRECTORY, "validations", "ko")
## END CHANGE

ROOT = "https://acordes.lacuerda.net"
URL_ARTIST_INDEX = "https://acordes.lacuerda.net/tabs/"
SONG_VERSION = 0
INDEX = "abcdefghijklmnopqrstuvwxyz#"

# (these globals are no longer really needed, but kept to avoid touching more code)
dir_list = list()
output_file = str()
dir = str()
file_name = str()


def validate_song_format(song):
    """Validates if the song follows a basic expected format + extra chord rule."""
    # Basic regex pattern for song format (original rule)
    pattern = r"((?:[A-Z]+\s+)*\n.+)+"

    # Check if the song matches the basic pattern
    match = re.fullmatch(pattern, song, flags=re.DOTALL)
    if not match:
        return False

    # EXTRA RULE: the song must contain at least one chord-only line
    if not has_chord_line(song):
        return False

    return True
    
def has_chord_line(song: str) -> bool:
    """Checks if the song contains at least one chord-only line (extra validation rule)."""
    chord_pattern = re.compile(
        r'^([A-G][#b]?(m|maj7|m7|7|sus2|sus4|dim|aug)?)(\s+[A-G][#b]?(m|maj7|m7|7|sus2|sus4|dim|aug)?)*$'
    )

    for line in song.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if chord_pattern.match(stripped):
            return True

    return False



## CHANGED: safer recursive file listing using os.walk, no global state
def list_files_recursive(path: str):
    """Lists all files in a directory recursively (safer version using os.walk)."""
    files = []
    for root, _, filenames in os.walk(path):
        for name in filenames:
            files.append(os.path.join(root, name))
    return files
## END CHANGE


@click.command()
@click.option(
    "--init",
    "-i",
    is_flag=True,
    default=False,
    help=(
        "If flag is present, drops all files and validates from the clean directory. "
    ),
)
def main(init):
    # Start time tracking
    start_time = datetime.datetime.now()
    log.info(f"Validator started at {start_time}")
    print("Starting validator...")

    if init:
        if os.path.exists(OUTPUT_DIRECTORY_OK):
            shutil.rmtree(OUTPUT_DIRECTORY_OK)
        if os.path.exists(OUTPUT_DIRECTORY_KO):
            shutil.rmtree(OUTPUT_DIRECTORY_KO)
        log.info("Directories Removed")

    OK = 0
    KO = 0

    for file_path in list_files_recursive(CLEANED_DIRECTORY):

        text = str()
        with open(file_path, "r") as file:
            text = file.read()

        # Formatting of the text goes in that function call
        validated = validate_song_format(text)

        ## CHANGED: compute relative path from CLEANED_DIRECTORY
        rel_path = os.path.relpath(file_path, CLEANED_DIRECTORY)
        ## END CHANGE

        if validated:
            base_dir = OUTPUT_DIRECTORY_OK
            OK += 1
        else:
            base_dir = OUTPUT_DIRECTORY_KO
            KO += 1

        ## CHANGED: build output path using base_dir + relative path
        output_file = os.path.join(base_dir, rel_path)
        ## END CHANGE

        ## CHANGED: create parent directory using os.path.dirname
        out_dir = os.path.dirname(output_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
            print("OKs =", OK, "-- KOs =", KO, "--", out_dir, "CREATED!!")
        ## END CHANGE

        with open(output_file, "w") as file:
            file.write(text)
            ## CHANGED: print only the file name using os.path.basename
            print("OKs =", OK, "-- KOs =", KO, "--", os.path.basename(output_file), "CREATED!!")
            ## END CHANGE

    log.info(f"OKs = {OK}, -- KOs = {KO}, --")
    end_time = datetime.datetime.now()
    log.info(f"Validator ended at {end_time}")
    duration = end_time - start_time
    log.info(f"Total duration: {duration}")
    print(
        f"Validator finished. Duration in seconds: {duration.total_seconds()}, that is {duration.total_seconds() / 60} minutes."
    )


if __name__ == "__main__":
    main()
