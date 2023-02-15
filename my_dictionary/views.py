from django.shortcuts import render
import requests
from retrying import retry
from decouple import config


def home(request):
    return render(request, 'home.html')


@retry(wait_fixed=5000, stop_max_attempt_number=3)
def search(request):
    word = request.GET['word']
    app_id = config("API_ID")
    app_key = config("API_KEY")
    language_code = 'en'

    url = f'https://od-api.oxforddictionaries.com:443/api/v2/entries/{language_code}/{word.lower()}'
    headers = {'app_id': app_id, 'app_key': app_key}
    result = requests.get(url, headers=headers, timeout=5)

    if result.status_code == 200:
        data = result.json()
        senses = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        definitions = [sense['definitions'][0] for sense in senses if 'definitions' in sense]
        synonyms = [synonym['text'] for sense in senses for synonym in sense.get('synonyms', [])]
    else:
        definitions = []
        synonyms = []

    results = {
        'word': word,
        'meaning': '\n\n'.join(str(x) for x in definitions),
    }

    # get antonyms using Merriam-Webster Dictionary
    url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
    api_key = config("MWEBAPI_KEY")

    response = requests.get(url + word, params={"key": api_key})
    if response.status_code == 200:
        data = response.json()
        # get the first definition object
        definition = data[0]
        # get the antonyms for the first definition
        antonyms = definition.get("meta", {}).get("ants")
        new_antonyms_list = [item for sublist in antonyms for item in sublist]
    else:
        new_antonyms_list = []

    # return syntax to return definition, synonyms and antonyms
    return render(request, 'search.html', {'se': synonyms, 'ae': new_antonyms_list, 'results': results})

    # return syntax for returning only definition and synonyms
    # return render(request, 'search.html', {'se': synonyms, 'results': results})
