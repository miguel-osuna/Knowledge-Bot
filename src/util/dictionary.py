# Standard library imports
import os
from os.path import dirname, abspath, join

# Third party imports
from dotenv import load_dotenv
from wordnik import swagger, WordApi, WordsApi

# Local application imports


BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
ENVIRONMENT = "local"
ENV_PATH = join(BASE_PROJECT_PATH, ".envs", f".{ENVIRONMENT}", ".application")

# Environment variable for wordnik
load_dotenv(ENV_PATH)
WORDNIK_API_URL = os.getenv("WORDNIK_API_URL")
WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")

api_url = WORDNIK_API_URL
api_key = WORDNIK_API_KEY

client = swagger.ApiClient(api_key, api_url)


def get_word_examples(
    word, include_duplicates=False, use_canonical=False, skip="", limit=5
):
    """ Returns sentences examples for a word. """
    word_client = WordApi.WordApi(client)
    example = word_client.getExamples(
        word,
        includeDuplicates=include_duplicates,
        useCanonical=use_canonical,
        skip=skip,
        limit=limit,
    )

    return example


def get_definition(
    word,
    limit=200,
    part_of_speech="",
    include_related=False,
    source_dictionaries="all",
    use_canonical=False,
    include_tags=False,
):
    """ Returns word definitions. """
    word_client = WordApi.WordApi(client)
    definition = word_client.getDefinitions(
        word=word,
        limit=limit,
        partOfSpeech=part_of_speech,
        includeRelated=include_related,
        useCanonical=use_canonical,
        includeTags=include_tags,
    )

    return definition


def get_synonyms(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns word synonyms. """
    relationship_types = "synonym"
    word_client = WordApi.WordApi(client)
    synonyms = word_client.getRelatedWords(
        word,
        useCanonical=use_canonical,
        relationshipTypes=relationship_types,
        limitPerRelationshipType=limit_per_relationship_type,
    )

    return synonyms


def get_antonyms(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns word antonyms. """
    relationship_types = "antonym"
    word_client = WordApi.WordApi(client)

    antonyms = word_client.getRelatedWords(
        word,
        useCanonical=use_canonical,
        relationshipTypes=relationship_types,
        limitPerRelationshipType=limit_per_relationship_type,
    )

    return antonyms


def get_similar_words(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns simlar words for a given word. """
    relationship_types = "related-word"
    word_client = WordApi.WordApi(client)

    similar_words = word_client.getRelatedWords(
        word,
        useCanonical=use_canonical,
        relationshipTypes=relationship_types,
        limitPerRelationshipType=limit_per_relationship_type,
    )

    return similar_words


def get_rhymes(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns rhymes for a given word. """
    relationship_types = "rhyme"
    word_client = WordApi.WordApi(client)

    rhymes = word_client.getRelatedWords(
        word,
        useCanonical=use_canonical,
        relationshipTypes=relationship_types,
        limitPerRelationshipType=limit_per_relationship_type,
    )

    return rhymes


def get_word_of_the_day():
    """ Gets the word of the day. """
    words_client = WordsApi.WordsApi(client)
    wotd = words_client.getWordOfTheDay()

    return wotd


def get_random_word():
    """ Gets a random word. """
    words_client = WordsApi.WordsApi(client)
    random_word = words_client.getRandomWord()

    return random_word


if __name__ == "__main__":
    pass
