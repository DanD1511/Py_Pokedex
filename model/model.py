import requests


class PokemonModel:

    def __init__(self):
        self.api_url = 'https://pokeapi.co/api/v2/'

    def get_pokemon_list(self, limit=12, offset=0):
        response = requests.get(f'{self.api_url}pokemon?limit={limit}&offset={offset}')
        if response.status_code == 200:
            return response.json()['results']
        else:
            return []

    def get_pokemon_details(self, name):
        response = requests.get(f'{self.api_url}pokemon/{name}')
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_evolutions(self, species_url):
        response = requests.get(species_url)
        if response.status_code == 200:
            species_data = response.json()
            evolution_chain_url = species_data['evolution_chain']['url']
            evolution_response = requests.get(evolution_chain_url)
            if evolution_response.status_code == 200:
                chain = evolution_response.json()['chain']
                evolutions = []
                while chain:
                    evo_name = chain['species']['name']
                    evo_id = chain['species']['url'].split('/')[-2]
                    evolutions.append((evo_name, evo_id))
                    chain = chain['evolves_to'][0] if chain['evolves_to'] else None
                return evolutions
        return []
