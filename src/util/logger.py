# Standard library imports
import os
from os.path import dirname, abspath, join
import logging
import logging.handlers as handlers

# Generate paths
BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
LOGS_PATH = join(BASE_PROJECT_PATH, "data", "output", "logs")


def generate_logger(module_name):
    # Create custom logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    file_name = join(LOGS_PATH, "discord.log")
    timed_file_handler = handlers.TimedRotatingFileHandler(
        filename=file_name,
        when="midnight",
        interval=1,
        encoding="utf-8",
        backupCount=60,
        delay=False,
        utc=False,
    )
    timed_file_handler.suffix = "%Y-%m-%d"
    console_handler = logging.StreamHandler()

    # Create formatter and add it to handler
    formatter = logging.Formatter(
        "[Line: {lineno}] [{asctime}] [{levelname}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )
    timed_file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(timed_file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = generate_logger(__name__)
    logger.warning("This is a warning log")
