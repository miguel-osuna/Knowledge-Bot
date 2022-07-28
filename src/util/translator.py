from os.path import dirname, abspath, join
import six

BASE_PROJECT_PATH = dirname(dirname(dirname((abspath(__file__)))))
TRANSLATION_KEY_PATH = join(BASE_PROJECT_PATH, ".envs", ".local")


def detect_language(text):
    """Detects the text's language."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        TRANSLATION_KEY_PATH + "/knowledge-bot-development-b8ed9d8c16cb.json"
    )

    result = translate_client.detect_language(text)
    return str(result["language"])


def list_languages(target_language="english"):
    """List alll languages available."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        TRANSLATION_KEY_PATH + "/knowledge-bot-development-b8ed9d8c16cb.json"
    ).from_service_account_json()

    languages = translate_client.get_languages(target_language=target_language)

    for language in languages:
        print("{name} ({language})".format(**language))


def translate_text(target_language, text, model="nmt"):
    """Translates text into the target language.

    Target must be an ISO 639-1 lanfuage code.
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        TRANSLATION_KEY_PATH + "/knowledge-bot-development-b8ed9d8c16cb.json"
    )

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can be a string or a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        values=text, target_language=target_language, model=model
    )

    return result["translatedText"]


if __name__ == "__main__":
    print(translate_text("en", "This is a test"))
    detect_language("Hola, esta es una prueba")
