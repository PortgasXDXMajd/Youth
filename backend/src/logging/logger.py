import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from src.core.config import BASE_DIR, get_settings


def _resolve_log_dir(raw_dir: str) -> Path:
    log_dir = Path(raw_dir)
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    except PermissionError:
        fallback_dir = BASE_DIR / "logs"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        return fallback_dir


def setup_logging() -> None:
    settings = get_settings()

    log_dir = _resolve_log_dir(settings.log_dir)
    log_file = log_dir / "app.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    rotating_file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=14,
        encoding="utf-8",
    )
    rotating_file_handler.suffix = "%Y-%m-%d"
    rotating_file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(settings.log_level.upper())
    root_logger.addHandler(rotating_file_handler)
    root_logger.addHandler(console_handler)
