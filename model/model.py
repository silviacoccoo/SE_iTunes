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

        self.best_solution=[]
        self.max_num_albums = 0

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

        """
        for id_a1,id_a2 in self._lista_album_connessi:
            # Devo controllare che gli album si trovino nella lista dei nodi
            if id_a1 in self.id_map and id_a2 in self.id_map:
                a1=self.id_map[id_a1]
                a2=self.id_map[id_a2]
                if self.G.has_node(a1) and self.G.has_node(a2):
                    self._edges.append((a1, a2)) # Aggiungo alla lista self._edges le tuple

        self.G.add_edges_from(self._edges)
        """

        all_edges = DAO.get_album_connessi() # lista tuple da 2 elementi che sono gli id
        for e in all_edges:
            if e[0] in self.id_map and e[1] in self.id_map:
                album1=self.id_map[e[0]]
                album2=self.id_map[e[1]]
                if self.G.has_node(album1) and self.G.has_node(album2):
                    self._edges.append((album1, album2))

        self.G.add_edges_from(self._edges)

    def get_num_nodes(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.number_of_edges()

    def get_nodes(self):
        return self.G.nodes()

    def get_connected_components(self,a):
        # Il parametro a è un oggetto
        set_connected_component_for_a=nx.node_connected_component(self.G,a) # é l'insieme dei nodi che fanno parte della componente connessa in cui c'è il nodo n
        # Insieme di nodi raggiungibili da n
        dimensione=len(set_connected_component_for_a)

        d_tot=0
        for s in set_connected_component_for_a: # Per ogni album, che è un oggetto
            d=float(s.durata_album)
            d_tot+=d

        return dimensione, d_tot, list(set_connected_component_for_a)

    # PUNTO 2 RICORSIONE
    def get_best_solution(self,a,d_tot):
        """ Prepara i dati e lancia la ricorsione"""

        # Reset variabili per la soluzione migliore
        self.best_solution=[]
        self.max_num_albums = 0

        # Recupero della componente connessa
        _, _, comp_connessa=self.get_connected_components(a) # a è un oggetto
        candidati= [ c for c in comp_connessa if c.id_album != a.id_album]
        # Lista di oggetti in ordine crescente
        candidati.sort(key=lambda x: x.durata_album) # Ordino in modo crescente

        parziale=[a]
        durata_iniziale=a.durata_album # Durata dell'album iniziale

        if durata_iniziale > d_tot: # Se già sfora la durata limite non lancio neanche la ricorsione
            return []

        # Lancio della ricorsione, i parametri devono essere inizializzati in questa funzione
        self.ricorsione(parziale,candidati,d_tot,durata_iniziale)
        # Deve ritornare un valore in quanto corrisponde alla funzione che chiamiamo nel controller alla pressione del pulsante
        return self.best_solution
        # RITORNA UNA LISTA BEST SOLUTION CHE SI AGGIORNA NELLA RICORSIONE

    def ricorsione(self,sol_parziale, album_rimanenti, durata_max, durata_corrente):
        # CASO TERMINALE: se supero il limite, mi fermo
        if durata_corrente>durata_max:
            return

        # Caso ricorsivo: in questo caso la soluzione è valida
        elif durata_corrente<=durata_max:

            # BEST SOLUTION CHECK --> SI AGGIORNA LA SOLUZIONE MIGLIORE
            if len(sol_parziale) > self.max_num_albums:
                self.max_num_albums=len(sol_parziale)
                self.best_solution=list(sol_parziale) # SE LA PARZIALE SODDISFA LE CONDIZIONI DIVENTA LA NUOVA BEST SOLUTION

            # ESPLORAZIONE: LOOP & BACKTRACKING --> SI POPOPLA LA SOLUZIONE PARZIALE
            for i, album in enumerate(album_rimanenti): # Itero sugli album rimanenti

                # AGGIUNGO ALLA PARZIALE GLI ELEMENTI
                sol_parziale.append(album)

                # RICORSION
                self.ricorsione(sol_parziale, album_rimanenti[i+1:],durata_max,durata_corrente+album.durata_album)

                # BACKTRACKING
                sol_parziale.pop()


