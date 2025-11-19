import os
import sys
import logging
import subprocess

# BASE_DIR = carpeta tab_processor (padre de pipeline)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

# Configuración de logging: a archivo + a consola
logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def path(*parts):
    """Construye una ruta relativa a tab_processor."""
    return os.path.join(BASE_DIR, *parts)


def run_step(name, command):
    logger.info(f"Starting: {name}")
    try:
        # Ejecutamos cada módulo desde la carpeta tab_processor
        subprocess.check_call(command, cwd=BASE_DIR)
        logger.info(f"Completed: {name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"FAILED: {name} - return code {e.returncode}")
        print(f"ERROR en {name}. Revisa logs/pipeline.log")
        raise
    except Exception as e:
        logger.exception(f"FAILED: {name} - {str(e)}")
        print(f"ERROR en {name}. Revisa logs/pipeline.log")
        raise


def main():
    logger.info("Pipeline execution started")

    run_step("SCRAPPER",  [sys.executable, path("scrapper", "main.py")])
    run_step("CLEANER",   [sys.executable, path("tab_cleaner", "main.py")])
    run_step("VALIDATOR", [sys.executable, path("tab_validator", "main.py")])
    run_step("RESULTS",   [sys.executable, path("results", "main.py")])
    run_step("LYRICS",    [sys.executable, path("lyrics", "main.py")])
    run_step("INSIGHTS",  [sys.executable, path("insights", "main.py")])

    logger.info("Pipeline execution finished successfully")
    print("Pipeline terminado correctamente.")


if __name__ == "__main__":
    main()
