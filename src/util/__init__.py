from .logger import generate_logger
from .paginator import Pages
from .dictionary import (
    get_word_examples,
    get_definition,
    get_synonyms,
    get_antonyms,
    get_similar_words,
    get_rhymes,
    get_word_of_the_day,
    get_random_word,
)
from .translator import detect_language, list_languages, translate_text

__all__ = [
    "generate_logger",
    "Pages",
    "get_word_examples",
    "get_definition",
    "get_synonyms",
    "get_antonyms",
    "get_similar_words",
    "get_rhymes",
    "get_word_of_the_day",
    "get_random_word",
    "detect_language",
    "list_languages",
    "translate_text",
]
