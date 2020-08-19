# Standard library imports
import six

# Third party imports

# Local application imports


def detect_language(text):
    """ Detects the text's language. """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        "/home/miguelosuna/Dev/Python/Knowledge-Bot/.envs/.local/knowledge-bot-development-b8ed9d8c16cb.json"
    )

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.

    result = translate_client.detect_language(text)

    print("Text : {}".format(text))
    print("Confidence: {}".format(result["confidence"]))
    print("Language: {}".format(result["language"]))


def list_languages(target_language="english"):
    """ List alll languages available. """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        "/home/miguelosuna/Dev/Python/Knowledge-Bot/.envs/.local/knowledge-bot-development-b8ed9d8c16cb.json"
    ).from_service_account_json()

    languages = translate_client.get_languages(target_language=target_language)

    for language in languages:
        print(u"{name} ({language})".format(**language))


def translate_text(target_language, text, model="nmt"):
    """ Translates text into the target language. 
    
    Target must be an ISO 639-1 lanfuage code.
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        "/home/miguelosuna/Dev/Python/Knowledge-Bot/.envs/.local/knowledge-bot-development-b8ed9d8c16cb.json"
    )

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can be a string or a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        values=text, target_language=target_language, model=model
    )

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected Source Language: {}".format(result["detectedSourceLanguage"]))


if __name__ == "__main__":
    pass
