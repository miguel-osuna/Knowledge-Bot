# Standard library imports
import os
from os.path import dirname, abspath, join

# Third party imports
from dotenv import load_dotenv

# Generate paths
ENVIRONMENT = "local"
BASE_PROJECT_PATH = dirname(dirname((abspath(__file__))))
ENV_PATH = join(BASE_PROJECT_PATH, ".envs", f".{ENVIRONMENT}", ".application")
LOGS_PATH = join(BASE_PROJECT_PATH, "data", "output", "logs")
LANGUAGES_PATH = join(BASE_PROJECT_PATH, "data", "input", "langs")
COGS_PATH = join(BASE_PROJECT_PATH, "src", "cogs")

# Loads environmental variables
load_dotenv(ENV_PATH)
TOKEN = os.getenv("DISCORD_TOKEN")
VERSION = os.getenv("VERSION")

if __name__ == "__main__":
    print("config file")
