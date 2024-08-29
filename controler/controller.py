class PokedexController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_page = 0
        self.view.set_controller(self)
        self.load_pokemon_list()

        # Connect signals
        self.view.search_button.clicked.connect(self.search_pokemon)
        self.view.prev_button.clicked.connect(self.previous_page)
        self.view.next_button.clicked.connect(self.next_page)

    def load_pokemon_list(self):
        pokemon_list = self.model.get_pokemon_list(limit=12, offset=self.current_page * 12)
        formatted_list = [{'name': pokemon['name'], 'image_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon['url'].split('/')[-2]}.png"} for pokemon in pokemon_list]
        self.view.display_pokemon_list(formatted_list)

    def search_pokemon(self):
        pokemon_name = self.view.input_field.text().strip().lower()
        if pokemon_name:
            pokemon_details = self.model.get_pokemon_details(pokemon_name)
            if pokemon_details:
                evolutions = self.model.get_evolutions(pokemon_details['species']['url'])
                self.view.display_pokemon_details(pokemon_details, evolutions)

    def handle_pokemon_selection(self, pokemon):
        self.search_pokemon(pokemon['name'])

    def next_page(self):
        """
        Advances to the next page of Pokémon.
        """
        self.current_page += 1
        self.load_pokemon_list()

    def previous_page(self):
        """
        Goes back to the previous page of Pokémon.
        """
        if self.current_page > 0:
            self.current_page -= 1
        self.load_pokemon_list()
