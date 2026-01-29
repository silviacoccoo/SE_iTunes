import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_album=None

    # PRIMO BOTTONE
    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            d=float(self._view.txt_durata.value)
        except ValueError:
            self._view.show_alert('Inserire valore numerico')
            return

        # Creo il grafo
        self._model.build_graph(d)
        self._current_album=None # RESET
        n_nodes = self._model.get_num_nodes()

        if n_nodes == 0:
            self._view.show_alert("Attenzione: Il grafo è vuoto! Prova con una durata inferiore.")

            # Pulisco comunque la vista e il dropdown per coerenza
            self._view.lista_visualizzazione_1.controls.clear()
            self.fill_dropdown()  # Questo svuoterà il menu
            self._view.update()
            return

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f'Grafo creato: {self._model.get_num_nodes()} album {self._model.get_num_edges()} archi')
        )

        # Una volta creato il grafo popoliamo il dropdown
        self.fill_dropdown()

        # Aggiornare sempre la pagina
        self._view.update()
        # TODO

    # QUESTA FUNZIONE DEVE ESSERE CHIAMATA ALTRIMENTI IL DROPDOWN NON SI POPOLA
    # La chiamo quando abbiamo creato il grafo e dunque abbiamo i nodi
    def fill_dropdown(self):
        """ Popola il dropdown con gli album presenti nel grafo """
        self._view.dd_album.options.clear()  # Ripulisco ogni volta l'album selezionato
        self._view.dd_album.value=None # Resetto

        all_albums = self._model.get_nodes()  # Ottengo tutti i nodi

        for a in all_albums:  # Per ogni nodo, cioè per ogni album
            option = ft.dropdown.Option(key=str(a.id_album),
                                        text=a.nome_album)  # I nodi sono già solo una stringa con il titolo dell'album
            self._view.dd_album.options.append(option)
            # Importante popolare il dropdown con una chiave che mi permette di identificare l'album univocamente
        self._view.dd_album.update()
        self._view.dd_album.on_change = self.get_selected_album

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # Quando si seleziona un album dal dropdown
        id_scelto=self._view.dd_album.value # L'id scelto per noi, il nome scelto per l'utente

        if id_scelto is None:
            self._current_album=None
            return

        # FARE LA MAPPATURA
        id_album=int(id_scelto) # Per essere una key nel dropdown doveva essere una stringa
        if id_album in self._model.id_map:
            self._current_album=self._model.id_map[id_album]
            print(f'Album selezionato {self._current_album}')
        # TODO

    # SECONDO BOTTONE
    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # Quando schiaccio il pulsante 'Analisi componente'

        if self._current_album is None:
            self._view.show_alert('Selezionare prima un album')
            return
        if self._current_album not in self._model.get_nodes():
            self._view.show_alert("L'album non fa parte del grafo")
            return

        dimensione, durata, _ =self._model.get_connected_components(self._current_album)

        self._view.lista_visualizzazione_2.controls.clear()  # Reset

        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f'Dimensione componente: {dimensione}'))
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f'Durata totale: {durata}'))
        self._view.update()
        # TODO

    # TERZO BOTTONE
    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # Parametri per get_best_solution

        a=self._current_album # Album inserito nel 2 riquadro
        if a is None:
            self._view.show_alert('Selezionare un album dal grafo!')
            return
        if a not in self._model.get_nodes():
            self._view.show_alert("L'album non fa parte del grafo")
            return

        d_tot_str=self._view.txt_durata_totale.value
        if not d_tot_str:
            self._view.show_alert('Inserire la durata totale massima!')
            return
        try:
            d_tot=float(d_tot_str) # Valore inserito nel 3 riquadro
        except ValueError:
            self._view.show_alert('Inserire un valore numerico')
            return

        best_set=self._model.get_best_solution(a, d_tot) # Lista di oggetti album

        self._view.lista_visualizzazione_3.controls.clear() # Reset

        if not best_set:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text('Nessun set trovato')
            )
        # Altrimenti
        durata_reale=sum(album.durata_album for album in best_set)

        self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f'Set trovato (album {len(best_set)}, durata {durata_reale:.2f} minuti):')
        )
        for album in best_set:
            self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f'-{album.nome_album} ({album.durata_album:.2f} min)')
        )

        self._view.update()
        # TODO