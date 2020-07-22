import logging

# Create custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
file_name = join(LOGS_PATH, "discord.log")
file_handler = logging.FileHandler(filename=file_name, encoding="utf-8", mode="a")
console_handler = logging.StreamHandler()

# Create formatter and add it to handler
formatter = logging.Formatter(
    "[{asctime}] [{levelname}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Testing logger
logger.warning("This is a warning")
logger.info("This is an info")
