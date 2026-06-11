import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fill_insights(self):
        top_five_tracks = self._model.get_top_five_tracks()
        top_five_artists = self._model.get_top_five_artists()
        top_five_genres = self._model.get_top_five_genres()

        self._view._top_tracks_col.controls.clear()
        self._view._top_artists_col.controls.clear()
        self._view._top_genres_col.controls.clear()

        self._view._top_tracks_col.controls.append(
            ft.Text("Top 5 Tracks", weight=ft.FontWeight.BOLD)
        )
        for track in top_five_tracks:
            self._view._top_tracks_col.controls.append(
                ft.Text(str(track))
            )

        self._view._top_artists_col.controls.append(
            ft.Text("Top 5 Artists", weight=ft.FontWeight.BOLD)
        )
        for artist in top_five_artists:
            self._view._top_artists_col.controls.append(
                ft.Text(str(artist))
            )

        self._view._top_genres_col.controls.append(
            ft.Text("Top 5 Genres", weight=ft.FontWeight.BOLD)
        )
        for genre in top_five_genres:
            self._view._top_genres_col.controls.append(
                ft.Text(str(genre))
            )
        num_clienti = self._model.get_num_customers()
        num_fatture = self._model.get_num_fatture()
        num_tracce = self._model.get_num_tracks()

        self._view._num_clienti.controls.clear()
        self._view._num_fatture.controls.clear()
        self._view._num_tracce.controls.clear()

        self._view._num_clienti.controls.append(
            ft.Text("Numero clienti", weight=ft.FontWeight.BOLD)
        )
        self._view._num_clienti.controls.append(
            ft.Text(str(num_clienti))
        )

        self._view._num_fatture.controls.append(
            ft.Text("Numero fatture", weight=ft.FontWeight.BOLD)
        )
        self._view._num_fatture.controls.append(
            ft.Text(str(num_fatture))
        )

        self._view._num_tracce.controls.append(
            ft.Text("Numero tracce", weight=ft.FontWeight.BOLD)
        )
        self._view._num_tracce.controls.append(
            ft.Text(str(num_tracce))
        )
        top_3_artist_with_more_different_clients = self._model.get_top_3_artist_with_more_different_clients()
        top_3_spenders = self._model.get_top_3_spenders()

        self._view._top_3_artist_with_more_different_client.controls.clear()
        self._view._top_3_artist_with_more_different_client.controls.append(
            ft.Text("Top 3 artisti con più clienti diversi:", weight=ft.FontWeight.BOLD)
        )
        for artist in top_3_artist_with_more_different_clients:
            self._view._top_3_artist_with_more_different_client.controls.append(ft.Text(str(artist)))
        self._view._top_3_spenders.controls.clear()
        self._view._top_3_spenders.controls.append(
            ft.Text("Top 3 clienti che hanno speso di più::", weight=ft.FontWeight.BOLD)
        )
        for client in top_3_spenders:
            self._view._top_3_spenders.controls.append(ft.Text(f"{client[0]} {client[1]}"))

        self._view.update_page()

    def handle_graph1(self, e):
        self._view._lv_graph1.controls.clear()
        self._view._lv_algo_graph1.controls.clear()


        data1 = self._view._data_graph1_1.value
        data2 = self._view._data_graph1_2.value
        genre = self._view._dd_genres.value

        if data1 is None or data2 is None or genre is None:
            self._view._lv_graph1.controls.append(
                ft.Text("Seleziona le date e un genere per proseguire.", color="red")
            )
            self._view.update_page()
            return

        if data1 > data2:
            self._view._lv_graph1.controls.append(
                ft.Text("Seleziona un intervallo di date esistente.", color="red")
            )
            self._view.update_page()
            return

        self._view._lv_graph1.controls.append(
            ft.Text(
                f"Intervallo di date selezionato: {data1} - {data2}\n"
                f"Genere selezionato: {genre}"
            )
        )


        self._model.buildGraph1(genre,data1, data2)
        self.fill_ddTracks_graph1()
        self._view._btn_algo_graph1.disabled = False

        self._view._lv_graph1.controls.append(
            ft.Text(
                f"Grafo correttamente creato\n"
                f"{self._model.printGraph1()}"
            )
        )
        top_bridge_tracks = self._model.get_top_bridge_tracks()

        self._view._lv_graph1.controls.append(
            ft.Text(
                "Top 3 brani più centrali (Betweenness Centrality)",
                weight=ft.FontWeight.BOLD
            )
        )

        for i, item in enumerate(top_bridge_tracks, start=1):
            self._view._lv_graph1.controls.append(
                ft.Text(
                    f"{i}) {item['track']}\n"
                    f"   Grado: {item['degree']}\n"
                    f"   Grado pesato: {item['weighted_degree']}\n"
                    f"   Centralità: {item['centrality']:.4f}"
                )
            )

        self._view.update_page()

    def handle_optPath_graph1(self, e):
        self._view._lv_algo_graph1.controls.clear()

        track_id = self._view._dd_track_graph1.value
        k = self._view._dd_k_graph1.value

        if track_id is None or k is None:
            self._view._lv_algo_graph1.controls.append(
                ft.Text("Seleziona un brano di partenza e un valore di k.", color="red")
            )
            self._view.update_page()
            return

        track_id = int(track_id)
        k = int(k)

        soluzione, score = self._model.get_optPath_coAcquisto(track_id, k)
        track_start = self._model._idMapNodes_1[track_id]

        self._view._lv_algo_graph1.controls.append(
            ft.Text(
                f"Percorso ottimo calcolato\n"
                f"Brano di partenza: {track_start.Name}\n"
                f"K brani: {k}\n"
                f"Score: {score}",
                weight=ft.FontWeight.BOLD
            )
        )

        for i, track in enumerate(soluzione, start=1):
            self._view._lv_algo_graph1.controls.append(
                ft.Text(f"{i}) {track}")
            )

        self._view.update_page()

    def fill_ddTracks_graph1(self):
        self._view._dd_track_graph1.options.clear()

        nodes = self._model.get_nodes_graph1()

        for track in nodes:
            self._view._dd_track_graph1.options.append(
                ft.dropdown.Option(
                    key=str(track.TrackId),
                    text=str(track)
                )
            )




    def fill_ddGenres(self):
        genres = self._model.get_name_genres()

        self._view._dd_genres.options.clear()

        for genre in genres:
            self._view._dd_genres.options.append(
                ft.dropdown.Option(genre)
            )

    #### Parte Grafo 2 ####

    def handle_graph2(self,e):
        self._view._lv_graph2.controls.clear()
        self._view._lv_algo_graph2.controls.clear()

        data1 = self._view._data_graph2_1.value
        data2 = self._view._data_graph2_2.value
        soglia = self._view._dd_soglia_graph2.value

        if data1 is None or data2 is None or soglia is None:
            self._view._lv_graph2.controls.append(
                ft.Text("Seleziona le date e un genere per proseguire.", color="red")
            )
            self._view.update_page()
            return

        if data1 > data2:
            self._view._lv_graph2.controls.append(
                ft.Text("Seleziona un intervallo di date esistente.", color="red")
            )
            self._view.update_page()
            return

        self._view._lv_graph2.controls.append(
            ft.Text(
                f"Intervallo di date selezionato: {data1} - {data2}\n"
                f"Soglia selezionata: {soglia}\n"
            )
        )
        soglia = int(soglia)

        self._model.buildGraph2(soglia, data1, data2)
        self._view._btn_algo_graph2.disabled = False
        self._view._lv_graph2.controls.append(
            ft.Text(
                f"Grafo correttamente creato\n"
                f"{self._model.printGraph2()}"
            )
        )
        top_artists = self._model.get_top_artists()

        self._view._lv_graph2.controls.append(
            ft.Text("Top 3 artisti più centrali", weight=ft.FontWeight.BOLD)
        )

        for i, (artist, degree, weighted_degree, centrality) in enumerate(top_artists, start=1):
            self._view._lv_graph2.controls.append(
                ft.Text(
                    f"{i}) {artist}\n"
                    f"   Grado: {degree}\n"
                    f"   Grado pesato: {weighted_degree}\n"
                    f"   Centralità: {centrality:.4f}"
                )
            )
        self._view.update_page()

    #metodo ottimizzazione grafo 2
    def handle_optPath_graph2(self, e):
        self._view._lv_algo_graph2.controls.clear()

        k_artisti = self._view._dd_k_artisti_graph2.value
        alfa = self._view._dd_alfa_graph2.value

        if k_artisti is None or alfa is None:
            self._view._lv_algo_graph2.controls.append(
                ft.Text("Seleziona il numero di artisti e il valore di alfa.", color="red")
            )
            self._view.update_page()
            return

        k_artisti = int(k_artisti)
        alfa = float(alfa)

        best_artists, best_score = self._model.get_optPath_Artisti(k_artisti, alfa)

        self._view._lv_algo_graph2.controls.append(
            ft.Text(
                "Funzione di score utilizzata:\n"
                "score = clienti_coperti - alfa * sovrapposizione",
                weight=ft.FontWeight.BOLD
            )
        )

        self._view._lv_algo_graph2.controls.append(
            ft.Text(
                f"Parametri selezionati:\n"
                f"Numero artisti: {k_artisti}\n"
                f"Alfa: {alfa}\n"
                f"Score migliore ottenuto: {best_score:.2f}"
            )
        )

        self._view._lv_algo_graph2.controls.append(
            ft.Text("Artisti selezionati:", weight=ft.FontWeight.BOLD)
        )

        for i, artist in enumerate(best_artists, start=1):
            self._view._lv_algo_graph2.controls.append(
                ft.Text(f"{i}) {artist}")
            )
        self._view.update_page()

    ### parte grafo 3 #####

    def handle_graph3(self, e):
        self._view._lv_graph3.controls.clear()
        self._view._lv_algo_graph3.controls.clear()

        soglia = self._view._dd_soglia_graph3.value

        if soglia is None:
            self._view._lv_graph3.controls.append(
                ft.Text("Seleziona una soglia per proseguire.", color="red")
            )
            self._view.update_page()
            return

        soglia = int(soglia)

        self._view._lv_graph3.controls.append(
            ft.Text(
                f"Soglia selezionata: {soglia}"
            )
        )

        self._model.buildGraph3(soglia)
        self._view._btn_algo_graph3.disabled = False

        self._view._lv_graph3.controls.append(
            ft.Text(
                f"Grafo correttamente creato\n"
                f"{self._model.printGraph3()}"
            )
        )

        representative_customers, outlier_customers = self._model.analyze_customer_segments()

        self._view._lv_graph3.controls.append(
            ft.Text(
                "Top 3 clienti più rappresentativi",
                weight=ft.FontWeight.BOLD
            )
        )

        for i, customer_data in enumerate(representative_customers, start=1):
            customer = customer_data["customer"]

            self._view._lv_graph3.controls.append(
                ft.Text(
                    f"{i}) {customer}\n"
                    f"   Grado: {customer_data['degree']}\n"
                    f"   Grado pesato: {customer_data['weighted_degree']}"
                )
            )

        self._view._lv_graph3.controls.append(
            ft.Text(
                "Clienti outlier",
                weight=ft.FontWeight.BOLD
            )
        )

        if len(outlier_customers) == 0:

            self._view._lv_graph3.controls.append(
                ft.Text("Nessun outlier individuato.")
            )

        else:

            for customer_data in outlier_customers:
                customer = customer_data["customer"]

                self._view._lv_graph3.controls.append(
                    ft.Text(
                        f"{customer}\n"
                        f"   Grado: {customer_data['degree']}\n"
                        f"   Grado pesato: {customer_data['weighted_degree']}"
                    )
                )

        self._view.update_page()

    def handle_optPath_graph3(self, e):

        self._view._lv_algo_graph3.controls.clear()

        k_clienti = self._view._dd_k_clienti_graph3.value
        alfa = self._view._dd_alfa_graph3.value

        if k_clienti is None or alfa is None:
            self._view._lv_algo_graph3.controls.append(
                ft.Text(
                    "Seleziona il numero di clienti e il valore di alfa.",
                    color="red"
                )
            )
            self._view.update_page()
            return

        k_clienti = int(k_clienti)
        alfa = float(alfa)

        best_clients, best_score = self._model.getOpt_Path_Clienti(
            k_clienti,
            alfa
        )

        self._view._lv_algo_graph3.controls.append(
            ft.Text(
                "Funzione di score utilizzata:",
                weight=ft.FontWeight.BOLD
            )
        )

        self._view._lv_algo_graph3.controls.append(
            ft.Text(
                "score = copertura - alfa * sovrapposizione"
            )
        )

        self._view._lv_algo_graph3.controls.append(
            ft.Text(
                f"Numero clienti selezionato: {k_clienti}\n"
                f"Alfa: {alfa}\n"
                f"Score migliore ottenuto: {best_score:.2f}"
            )
        )

        self._view._lv_algo_graph3.controls.append(
            ft.Text(
                "Clienti selezionati:",
                weight=ft.FontWeight.BOLD
            )
        )

        for i, customer in enumerate(best_clients, start=1):
            self._view._lv_algo_graph3.controls.append(
                ft.Text(
                    f"{i}) {customer}"
                )
            )

        self._view.update_page()
















