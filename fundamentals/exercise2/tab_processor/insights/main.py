from pathlib import Path
from collections import Counter, defaultdict
import re

# Directorio base de las letras ya validadas y limpias
LYRICS_ROOT = Path("files/validations/ok/cleaned/songs")
OUTPUT_DIR = Path("files/insights")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def normalize_word(word: str) -> str:
    """
    Normaliza una palabra:
    - Pasa a minúsculas
    - Elimina caracteres no alfabéticos
    """
    word = word.lower()
    # Nos quedamos solo con letras (sin números ni signos)
    word = re.sub(r"[^a-záéíóúüñ]", "", word)
    return word


# Lista rápida de palabras vacías en español para filtrar
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "y", "o", "u", "de", "del", "al", "a", "en", "por", "para",
    "con", "sin", "que", "como", "se", "me", "te", "lo", "le",
    "mi", "mis", "tu", "tus", "su", "sus", "nos", "vos",
    "ya", "no", "si", "sí", "pero", "más", "mas"
}


def extract_words(text: str):
    """
    Extrae palabras 'contenido' de un texto:
    - Normaliza
    - Filtra vacías y muy cortas
    (Aproximamos sustantivos/verbos/adjetivos eliminando palabras vacías)
    """
    raw_tokens = text.split()
    words = []
    for tok in raw_tokens:
        w = normalize_word(tok)
        if len(w) <= 2:
            continue
        if w in STOPWORDS:
            continue
        words.append(w)
    return words


def main():
    if not LYRICS_ROOT.exists():
        print(f"Directory not found: {LYRICS_ROOT}")
        return

    # 1) Leer todas las letras por artista
    artist_texts = defaultdict(list)
    total_text = []

    for lyrics_file in LYRICS_ROOT.rglob("*_lyrics.txt"):
        # parent.name = nombre del artista
        artist = lyrics_file.parent.name
        try:
            text = lyrics_file.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Error reading {lyrics_file}: {e}")
            continue

        artist_texts[artist].append(text)
        total_text.append(text)

    if not artist_texts:
        print("No lyrics files found.")
        return

    print("Merging lyrics and computing insights...\n")

    # 2) Fusionar letras y escribir un archivo por artista
    artist_word_counts = {}

    for artist, texts in artist_texts.items():
        merged_text = "\n\n".join(texts)

        # Guardar letras fusionadas por artista
        merged_path = OUTPUT_DIR / f"{artist}_all_lyrics.txt"
        merged_path.write_text(merged_text, encoding="utf-8")

        # Contar palabras del artista
        words = extract_words(merged_text)
        counter = Counter(words)
        artist_word_counts[artist] = counter

    # 3) Contar globalmente
    global_text = "\n\n".join(total_text)
    global_words = extract_words(global_text)
    global_counter = Counter(global_words)

    # 4) Mostrar resultados por artista (top 10)
    print("Top 10 palabras por artista\n")
    for artist, counter in sorted(artist_word_counts.items()):
        print(f"Artista: {artist}")
        for i, (word, freq) in enumerate(counter.most_common(10), start=1):
            print(f"  {i}. {word}: {freq}")
        print()

    # 5) Mostrar resultados globales (top 20)
    print("Top 20 palabras globales\n")
    for i, (word, freq) in enumerate(global_counter.most_common(20), start=1):
        print(f"  {i}. {word}: {freq}")

    # 6) También guardamos los resultados en archivos de texto
    #    Un archivo por artista con su top-10
    for artist, counter in artist_word_counts.items():
        out_path = OUTPUT_DIR / f"{artist}_top10_words.txt"
        lines = [
            f"Top 10 palabras para el artista: {artist}\n",
        ]
        for i, (word, freq) in enumerate(counter.most_common(10), start=1):
            lines.append(f"{i}. {word}: {freq}\n")
        out_path.write_text("".join(lines), encoding="utf-8")

    #    Archivo global con el top-20
    global_out = OUTPUT_DIR / "global_top20_words.txt"
    lines = ["Top 20 palabras globales:\n"]
    for i, (word, freq) in enumerate(global_counter.most_common(20), start=1):
        lines.append(f"{i}. {word}: {freq}\n")
    global_out.write_text("".join(lines), encoding="utf-8")

    print("\nInsights finished.")
    print(f"Outputs saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
