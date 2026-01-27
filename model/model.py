import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph() # Semplice non orientato e non pesato
        self._nodes=[]
        self._edges=[]

        self.id_map={}
        self._lista_album_validi=[]
        self._lista_album_connessi=[]

        # Importantissimo chiamare queste funzioni
        # Se non le chiamassi le liste sarebbero vuote e non verrebbe popolato il grafo !!!
        self.load_album_validi() # Devo chiamarlo, altrimenti la funzione build graph itera su una lista vuota

    # Gli album che faranno parte del grafo come vertici
    def load_album_validi(self):
        self._lista_album_validi=DAO.get_album_validi()
        # Lista di dizionari con id album e sua durata totale
        self.id_map = {}
        for album in self._lista_album_validi:
            self.id_map[album.id_album]=album
            # Chiave id album, valore associato l'oggetto album

    def load_album_connessi(self):
        self._lista_album_connessi=DAO.get_album_connessi()

    def build_graph(self, d):
        self.G.clear()
        self._nodes=[]
        self._edges=[]

        # Lista album validi è una lista di oggetti
        # Aggiungiamo i vertici
        for a in self._lista_album_validi:
            if float(a.durata_album)>d:
                self._nodes.append(a.id_album)
        self.G.add_nodes_from(self._nodes)
        # self._nodes è una lista

        # Aggiungiamo gli archi
        # Lista album connessi è una lista di tuple (id_album1, id_album2)
        # Non è vuota perchè l'ho chiamata nell' __init__
        if not self._lista_album_connessi:
            self.load_album_connessi()

        for a1,a2 in self._lista_album_connessi:
            # Devo controllare che gli album si trovino nella lista dei nodi
            if a1 in self._nodes and a2 in self._nodes:
                self._edges.append((a1, a2)) # Aggiungo alla lista self._edges le tuple

        self.G.add_edges_from(self._edges)

    def get_num_nodes(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.number_of_edges()

    def get_nodes(self):
        return self.G.nodes()