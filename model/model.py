import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph() # Semplice non orientato e non pesato
        self._nodes=[]
        self._edges=[]

        self._lista_album=[]
        self._lista_album_validi=[]
        self._lista_album_connessi=[]

    def load_album(self):
        self._lista_album=DAO.get_album()
        # Lista di tuple album e canzone

    def load_album_validi(self):
        self._lista_album_validi=DAO.get_album_validi()
        # Lista di dizionari con id album e sua durata totale

    def load_album_connessi(self):
        self._lista_album_connessi=DAO.get_album_connessi()
        # ???

    def build_graph(self, d):
        self.G.clear()
        self._nodes=[]
        self._edges=[]

        # Aggiungiamo i vertici
        for a in self._lista_album_validi:
            if float(float(a['durata_album'])/60)>d:
                self._nodes.append(a)
        self.G.add_nodes_from(self._nodes)

        # Aggiungiamo gli archi
        edges={}

    def get_num_nodes(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.number_of_edges()

