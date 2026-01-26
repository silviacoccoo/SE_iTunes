import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    # PRIMO BOTTONE
    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # Creo il grafo
        d=float(self._view.txt_durata.value)
        self._model.build_graph(d)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f'Grafo creato: {self._model.get_num_nodes()} album {self._model.get_num_edges()} archi')
        )
        self._view.update()
        # TODO

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO

    # SECONDO BOTTONE
    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO

    # TERZO BOTTONE
    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO