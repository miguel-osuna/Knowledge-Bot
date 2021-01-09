import os
from os.path import dirname, abspath, join

# Generate paths
BASE_PROJECT_PATH = dirname(dirname((abspath(__file__))))
LANGUAGES_PATH = join(BASE_PROJECT_PATH, "data", "input", "langs")
COGS_PATH = join(BASE_PROJECT_PATH, "src", "cogs")

# Loads environmental variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VERSION = os.getenv("VERSION")
SUPPORT_SERVER_INVITE_URL = os.getenv("SUPPORT_SERVER_INVITE_URL")
BOT_INVITE_URL = os.getenv("BOT_INVITE_URL")
COMMAND_PREFIX = str(os.getenv("COMMAND_PREFIX"))

# Wordnik variables
WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")
WORDNIK_API_URL = os.getenv("WORDNIK_API_URL")
