## Install dependencies
For installing needed dependencies, run `pip install -r requirements.txt`

## Go to the tab_processor directory in the terminal
To navigate to the tab_processor directory, run:
```bash
cd 'path/to/tab_processor'
```
or in vs code, right click on the `tab_processor` folder and select "Open in Integrated Terminal".

## Run the scrapper
To run the scrapper and reload the catalog, execute:

```bash
python scrapper/main.py
``` 
This will create a directory `files`. A `catalog.json` will be created inside, and a `songs` directory will be created. The `songs` directory will contain the downloaded tabs, and the `catalogs` directory will contain the catalogs of songs.

If you want to download tabs for a specific letters range, you can use the `-sc` and `-ec` options, stating or 'start char' and 'end char'. For example, to download tabs for artists starting with letters from A to C, execute:

```bash
python scrapper/main.py -sc a -ec c
```

## Clean the tabs
To clean the downloaded tabs, execute:
```bash
python tab_cleaner/main.py
```
This will create a subdirectory `cleaned` inside the `files` directory, containing the cleaned tabs.

## Validate the cleaned tabs
To validate the cleaned tabs, execute:
```bash
python tab_validator/main.py
```
This will create two subdirectories inside the `files` directory: `validations/ok` and `validations/ko`. The `ok` directory will contain the valid tabs, and the `ko` directory will contain the invalid tabs.


## Response to the exercise:

1) (scraper) Modify get_songs in songs.py to use the catalog instead of scraping again. (2 points)

The function has been updated in the code. You can see both the old implementation and the new version.

2) (scraper) Check the logs for anything strange. Try to determine where those messages come from. You do not need to fix it, just identify the origin. (0.5 points)

Several issues can be observed:
Many songs are being installed again even though they were already downloaded previously.
Some song titles differ from the actual ones.
Some log messages are incorrect. For example, it says it will install lyrics from a certain source, but the real source is: acordes.lacuerda.net.

3) (cleaner) The cleaner is also receiving the catalogs as input. Although it is not a problem yet, we should avoid it. Implement a solution. (0.5 points)

I changed a function so that it only processes .txt files instead of attempting to process JSON files.

4) (validator) There is an issue when reading/saving files, as more directories than necessary are being created. (0.5 points)

5) (validator) Implement an additional validation rule. (0.5 points)
In addition to the original regex-based check, the validator now enforces that a song must contain at least one chord-only line.

A helper function has_chord_line(song) was added to detect lines consisting only of chords (A–G, optional #/b, and suffixes such as m, 7, maj7, sus4, etc.).

validate_song_format now first applies the original pattern and then calls has_chord_line. If no chord-only line is found, the song is marked as invalid (KO).

6) Propose improvements to make the code cleaner, clearer, and better. (0.5 points)
Some small changes could make the code clearer and easier to maintain:

- Avoid repeating the same file-handling code by moving it into a small helper function.
- Add basic type hints to make the functions easier to understand.
- Reduce the number of global variables by grouping paths into a single config section.
- Add short docstrings to explain what each function does.
- Unify the logging format so all modules print consistent messages.

## Funcionalidades que se deben añadir:

1) Additional Required Features
A new Python module named results was created to verify how many files we have at each stage of the pipeline.
It counts the total number of files (recursively) inside the main output directories:

files/songs/ → downloaded raw tabs
files/cleaned/ → cleaned tabs
files/validations/ok/ → valid tabs
files/validations/ko/ → invalid tabs

2) Add a new Python module called lyrics that removes all chords from the correctly validated files and stores the output in the appropriate directory. (2 points)
A new module called lyrics was added.
It processes all the files inside files/validations/ok/ and generates a new version of each song without chords, keeping only the lyrics.

3) Add a new Python module called insights that merges all OK lyrics into a single file per artist.
A new module called `insights` was added.

- The top 10 most frequent words (content words) for each artist.
- The top 20 most frequent words globally across all artists.

The merged lyrics and statistics are saved in the `files/insights` directory.

4) Create a Python script that runs all modules in order. It must have its own log file and record any failures. (1 point)
A new script called pipeline.py was added.
It runs all the modules in order (scrapper, tab_cleaner, tab_validator, results, lyrics and insights) and logs the whole execution in logs/pipeline.log. If any step fails, the error is recorded in this log file.