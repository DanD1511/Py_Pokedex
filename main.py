import sys
from PyQt6.QtWidgets import QApplication

from controler.controller import PokedexController
from model.model import PokemonModel
from view.view import PokedexView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = PokemonModel()
    view = PokedexView()
    controller = PokedexController(model, view)
    view.show()
    sys.exit(app.exec())
