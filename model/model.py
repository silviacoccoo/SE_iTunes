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
                self._nodes.append(a) # Aggiungo l'oggetto
        self.G.add_nodes_from(self._nodes)
        # self._nodes è una lista di oggetti

        # Aggiungiamo gli archi
        # Lista album connessi è una lista di tuple (id_album1, id_album2)
        # Non è vuota perchè l'ho chiamata nell' __init__
        if not self._lista_album_connessi:
            self.load_album_connessi() # Carico gli archi che non ci sono ancora

        for id_a1,id_a2 in self._lista_album_connessi:
            # Devo controllare che gli album si trovino nella lista dei nodi
            if id_a1 in self.id_map and id_a2 in self.id_map:
                a1=self.id_map[id_a1]
                a2=self.id_map[id_a2]
                if self.G.has_node(a1) and self.G.has_node(a2):
                    self._edges.append((a1, a2)) # Aggiungo alla lista self._edges le tuple

        self.G.add_edges_from(self._edges)

    def get_num_nodes(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.number_of_edges()

    def get_nodes(self):
        return self.G.nodes()

    def get_connected_components(self,a):
        set_connected_component_for_a=nx.node_connected_component(self.G,a) # é l'insieme dei nodi che fanno parte della componente connessa in cui c'è il nodo n
        # Insieme di nodi raggiungibili da n
        dimensione=len(set_connected_component_for_a)

        d_tot=0
        for s in set_connected_component_for_a: # Per ogni album, che è un oggetto
            d=float(s.durata_album)
            d_tot+=d

        return dimensione, d_tot
