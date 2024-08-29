from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests


class PokedexView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex PyQt6")
        self.setGeometry(100, 100, 1200, 600)
        self.setObjectName("main_window")
        self.setup_ui()
        self.load_styles()

    def load_styles(self):
        try:
            with open('styles/styles.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Could not load 'styles.css'. Ensure the file exists in the same directory.")

    def setup_ui(self):
        main_layout = QHBoxLayout()

        # Left page: Pokémon details
        self.details_page = QFrame(self)
        self.details_page.setObjectName("left_page")
        self.details_page.setFixedWidth(400)
        self.details_layout = QVBoxLayout(self.details_page)

        # Right page: Pokémon list
        self.list_page = QFrame(self)
        self.list_page.setObjectName("right_page")
        self.list_layout = QVBoxLayout(self.list_page)

        # Search input field
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter Pokémon name or ID")
        self.input_field.setStyleSheet("padding: 8px; border: 1px solid #333; border-radius: 5px; background-color: #333; color: white;")
        self.list_layout.addWidget(self.input_field)

        # Search button
        self.search_button = QPushButton("Search Pokémon", self)
        self.search_button.setStyleSheet("background-color: #e63946; color: white; padding: 8px; border-radius: 5px;")
        self.list_layout.addWidget(self.search_button)

        # Scroll area to display Pokémon
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #ffffff;")
        self.pokemon_container = QWidget()
        self.pokemon_layout = QGridLayout(self.pokemon_container)
        self.scroll_area.setWidget(self.pokemon_container)
        self.list_layout.addWidget(self.scroll_area)

        # Page navigation buttons
        self.navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous Page", self)
        self.next_button = QPushButton("Next Page", self)
        self.navigation_layout.addWidget(self.prev_button)
        self.navigation_layout.addWidget(self.next_button)
        self.list_layout.addLayout(self.navigation_layout)

        # Add pages to the main layout
        main_layout.addWidget(self.details_page)
        main_layout.addWidget(self.list_page)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def display_pokemon_list(self, pokemon_list):
        self.clear_layout(self.pokemon_layout)

        for index, pokemon_data in enumerate(pokemon_list):
            card = QFrame(self)
            card.setObjectName("pokemon-card")
            card_layout = QVBoxLayout(card)

            # Pokémon image
            image_label = QLabel(self)
            image_url = pokemon_data['image_url']
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(image_url).content)
            image_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Pokémon name
            name_label = QLabel(pokemon_data['name'].capitalize(), self)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

            # Card click event
            card.mousePressEvent = lambda event, pokemon=pokemon_data: self.on_card_clicked(pokemon)

            card_layout.addWidget(image_label)
            card_layout.addWidget(name_label)
            self.pokemon_layout.addWidget(card, index // 4, index % 4)

    def display_pokemon_details(self, pokemon_details, evolutions):
        self.clear_layout(self.details_layout)

        # Pokémon image
        image_label = QLabel(self.details_page)
        image_url = pokemon_details['sprites']['front_default']
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(image_url).content)
        image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_layout.addWidget(image_label)

        # Basic information
        info_label = QLabel(f"Name: {pokemon_details['name'].capitalize()}\n"
                            f"ID: {pokemon_details['id']}\n"
                            f"Height: {pokemon_details['height'] / 10} m\n"
                            f"Weight: {pokemon_details['weight'] / 10} kg", self.details_page)
        info_label.setStyleSheet("font-size: 12px; color: white;")
        self.details_layout.addWidget(info_label)

        # Abilities
        abilities_label = QLabel("Abilities:", self.details_page)
        abilities_label.setStyleSheet("font-weight: bold; color: white;")
        self.details_layout.addWidget(abilities_label)

        for ability in pokemon_details['abilities']:
            ability_label = QLabel(f"• {ability['ability']['name'].capitalize()}", self.details_page)
            ability_label.setStyleSheet("color: white;")
            self.details_layout.addWidget(ability_label)

        # Stats
        stats_label = QLabel("Stats:", self.details_page)
        stats_label.setStyleSheet("font-weight: bold; color: white;")
        self.details_layout.addWidget(stats_label)

        for stat in pokemon_details['stats']:
            stat_label = QLabel(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}", self.details_page)
            stat_label.setStyleSheet("color: white;")
            self.details_layout.addWidget(stat_label)

        # Evolutions
        if evolutions:
            evolutions_label = QLabel("Evolutions:", self.details_page)
            evolutions_label.setStyleSheet("font-weight: bold; color: white; text-align: center;")
            self.details_layout.addWidget(evolutions_label)

            for evo_name, evo_id in evolutions:
                evo_image_label = QLabel(self.details_page)
                evo_image_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{evo_id}.png'
                evo_pixmap = QPixmap()
                evo_pixmap.loadFromData(requests.get(evo_image_url).content)
                evo_image_label.setPixmap(evo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
                evo_image_label.setStyleSheet("margin: 5px;")
                evo_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.details_layout.addWidget(evo_image_label)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def on_card_clicked(self, pokemon):
        self.controller.handle_pokemon_selection(pokemon)

    def set_controller(self, controller):
        self.controller = controller
