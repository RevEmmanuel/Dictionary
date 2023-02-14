from django.shortcuts import render
import requests
from retrying import retry


def home(request):
    return render(request, 'home.html')


@retry(wait_fixed=5000, stop_max_attempt_number=3)
def search(request):
    word = request.GET['word']
    app_id = '5c856024'
    app_key = '1f2d433e10f3b7cb46816e854f939e79'
    language_code = 'en'

    url = f'https://od-api.oxforddictionaries.com:443/api/v2/entries/{language_code}/{word.lower()}'
    headers = {'app_id': app_id, 'app_key': app_key}
    result = requests.get(url, headers=headers, timeout=5)

    if result.status_code == 200:
        data = result.json()
        senses = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        definitions = [sense['definitions'][0] for sense in senses if 'definitions' in sense]
        synonyms = [synonym['text'] for sense in senses for synonym in sense.get('synonyms', [])]
        # antonyms = [antonym['text'] for sense in senses for antonym in sense.get('antonyms', [])]
    else:
        definitions = []
        synonyms = []
        # antonyms = []

    results = {
        'word': word,
        'meaning': '\n\n'.join(str(x) for x in definitions),
    }

    # return render(request, 'search.html', {'se': synonyms, 'ae': antonyms, 'results': results})
    return render(request, 'search.html', {'se': synonyms, 'results': results})
