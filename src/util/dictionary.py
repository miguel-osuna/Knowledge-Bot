import os
from os.path import dirname, abspath, join
from datetime import datetime

from wordnik import swagger, WordApi, WordsApi

WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")
WORDNIK_API_URL = os.getenv("WORDNIK_API_URL")

client = swagger.ApiClient(WORDNIK_API_KEY, WORDNIK_API_URL)


def get_word_examples(
    word, include_duplicates=False, use_canonical=False, limit=5, skip=None
):
    """ Returns sentences examples for a word. """
    word_client = WordApi.WordApi(client)

    # Create dictionary for keyword arguments
    data = {
        "word": word,
        "includeDuplicates": include_duplicates,
        "useCanonical": use_canonical,
        "limit": limit,
    }

    if skip is not None:
        data["skip"] = skip

    examples = word_client.getExamples(**data).examples
    examples_list = [example.text for example in examples]

    return examples_list


def get_definition(
    word,
    limit=200,
    include_related=False,
    source_dictionaries=["all"],
    use_canonical=False,
    include_tags=False,
    part_of_speech=None,
):

    """ Returns word definitions. """
    word_client = WordApi.WordApi(client)

    # Create dictionary for keyword arguments
    data = {
        "word": word,
        "limit": limit,
        "includeRelated": include_related,
        "sourceDictionaries": source_dictionaries,
        "useCanonical": use_canonical,
        "includeTags": include_tags,
    }

    if part_of_speech is not None:
        data["partOfSpeech"] = part_of_speech

    definitions = word_client.getDefinitions(**data)
    definitions_list = [
        definition.text for definition in definitions if definition.text != None
    ]

    return definitions_list


def get_synonyms(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns word synonyms. """
    word_client = WordApi.WordApi(client)

    data = {
        "word": word,
        "useCanonical": use_canonical,
        "relationshipTypes": "synonym",
        "limitPerRelationshipType": limit_per_relationship_type,
    }

    synonyms = word_client.getRelatedWords(**data)
    synonyms_list = synonyms[0].words

    return synonyms_list


def get_antonyms(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns word antonyms. """
    word_client = WordApi.WordApi(client)

    data = {
        "word": word,
        "useCanonical": use_canonical,
        "relationshipTypes": "antonym",
        "limitPerRelationshipType": limit_per_relationship_type,
    }

    antonyms = word_client.getRelatedWords(**data)
    antonyms_list = antonyms[0].words

    return antonyms_list


def get_similar_words(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns simlar words for a given word. """
    word_client = WordApi.WordApi(client)

    data = {
        "word": word,
        "useCanonical": use_canonical,
        "relationshipTypes": "related-word",
        "limitPerRelationshipType": limit_per_relationship_type,
    }

    similar_words = word_client.getRelatedWords(**data)
    similar_words_list = similar_words[0].words

    return similar_words_list


def get_rhymes(word, use_canonical=False, limit_per_relationship_type=10):
    """ Returns rhymes for a given word. """
    word_client = WordApi.WordApi(client)

    data = {
        "word": word,
        "useCanonical": use_canonical,
        "relationshipTypes": "rhyme",
        "limitPerRelationshipType": limit_per_relationship_type,
    }

    rhymes = word_client.getRelatedWords(**data)
    rhymes_list = rhymes[0].words

    return rhymes_list


def get_word_of_the_day():
    """ Get the word of the day with its definition. """
    words_client = WordsApi.WordsApi(client)

    today = datetime.today().strftime("%Y-%m-%d")
    random_word = words_client.getWordOfTheDay(date=today)

    word = random_word.word
    definitions = [
        definition.text
        for definition in random_word.definitions
        if definition.text is not None
    ]

    return word, definitions


def get_random_word():
    """ Gets a random word (without definition). """
    words_client = WordsApi.WordsApi(client)
    random_word = words_client.getRandomWord()
    return random_word.word


if __name__ == "__main__":
    print(get_definition("ball"))
