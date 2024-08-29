import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
import requests

class Pokedex(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex")
        self.setGeometry(100, 100, 400, 300)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Configurar el diseño
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Campo de entrada para el nombre del Pokémon
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Introduce el nombre o ID del Pokémon")
        self.layout.addWidget(self.input_field)

        # Botón de búsqueda
        self.search_button = QPushButton("Buscar Pokémon", self)
        self.search_button.clicked.connect(self.search_pokemon)
        self.layout.addWidget(self.search_button)

        # Área de texto para mostrar la información del Pokémon
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def search_pokemon(self):
        # Obtener el nombre o ID del campo de entrada
        pokemon_name = self.input_field.text().strip().lower()

        if not pokemon_name:
            self.result_area.setText("Por favor, introduce un nombre o ID de Pokémon.")
            return

        # Realizar la solicitud GET a la PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)

        if response.status_code == 200:
            # Obtener los datos del Pokémon
            data = response.json()
            name = data['name']
            id_ = data['id']
            height = data['height']
            weight = data['weight']
            types = ', '.join([t['type']['name'] for t in data['types']])

            # Mostrar la información del Pokémon en el área de texto
            info = (f"Nombre: {name.capitalize()}\n"
                    f"ID: {id_}\n"
                    f"Altura: {height / 10} m\n"
                    f"Peso: {weight / 10} kg\n"
                    f"Tipos: {types.capitalize()}")
            self.result_area.setText(info)
        else:
            self.result_area.setText(f"Pokémon '{pokemon_name}' no encontrado. Inténtalo de nuevo.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Pokedex()
    window.show()
    sys.exit(app.exec())
