import requests


class RequestsJSONDecodeError(Exception):
    pass


def find_pokemon(name):
    try:
        URL = f'https://pokeapi.co/api/v2/pokemon/{name}'
        params = {}
        response = requests.get(URL, params=params)
        result = response.json()
        return {'name': result['name'], 'type': result['types'][0]['type']['name'], 'id': result['id'],
                'height': result['height'], 'weight': result['weight'],
                'base_experience': result['base_experience']}
    except RequestsJSONDecodeError:
        return None
