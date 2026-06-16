import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _header(self, title, icon, subtitle=None):
        controls = [
            ft.Row(
                controls=[
                    ft.Icon(icon, color="#0F766E", size=20),
                    ft.Text(title, weight=ft.FontWeight.BOLD, color="#0F172A", size=15, selectable=True),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
        if subtitle is not None:
            controls.append(ft.Text(subtitle, color="#64748B", size=12, selectable=True))
        return controls

    def _add_ranked_items(self, column, items, accent):
        for i, item in enumerate(items, start=1):
            column.controls.append(self._view.create_rank_item(i, item, accent))

    def fill_insights(self):
        top_five_tracks = self._model.get_top_five_tracks()
        top_five_artists = self._model.get_top_five_artists()
        top_five_genres = self._model.get_top_five_genres()

        self._view._top_tracks_col.controls.clear()
        self._view._top_artists_col.controls.clear()
        self._view._top_genres_col.controls.clear()

        self._view._top_tracks_col.controls.extend(
            self._header("Top 5 brani", ft.icons.LIBRARY_MUSIC, "I brani piu acquistati")
        )
        self._add_ranked_items(self._view._top_tracks_col, top_five_tracks, "#0F766E")

        self._view._top_artists_col.controls.extend(
            self._header("Top 5 artisti", ft.icons.MIC_EXTERNAL_ON, "Gli artisti con piu vendite")
        )
        self._add_ranked_items(self._view._top_artists_col, top_five_artists, "#2563EB")

        self._view._top_genres_col.controls.extend(
            self._header("Top 5 generi", ft.icons.ALBUM, "I generi piu presenti negli acquisti")
        )
        self._add_ranked_items(self._view._top_genres_col, top_five_genres, "#F59E0B")

        num_clienti = self._model.get_num_customers()
        num_fatture = self._model.get_num_fatture()
        num_tracce = self._model.get_num_tracks()

        self._view._num_clienti.controls.clear()
        self._view._num_fatture.controls.clear()
        self._view._num_tracce.controls.clear()

        self._view._num_clienti.controls.append(
            self._view.create_metric_value("Clienti", num_clienti, ft.icons.PERSON_OUTLINE, "#0F766E")
        )
        self._view._num_fatture.controls.append(
            self._view.create_metric_value("Fatture", num_fatture, ft.icons.RECEIPT_LONG, "#2563EB")
        )
        self._view._num_tracce.controls.append(
            self._view.create_metric_value("Tracce", num_tracce, ft.icons.MUSIC_NOTE, "#F59E0B")
        )

        top_3_artist_with_more_different_clients = self._model.get_top_3_artist_with_more_different_clients()
        top_3_spenders = self._model.get_top_3_spenders()

        self._view._top_3_artist_with_more_different_client.controls.clear()
        self._view._top_3_artist_with_more_different_client.controls.extend(
            self._header(
                "Artisti con piu clienti diversi",
                ft.icons.DIVERSITY_2,
                "Top 3 per ampiezza del pubblico",
            )
        )
        self._add_ranked_items(
            self._view._top_3_artist_with_more_different_client,
            top_3_artist_with_more_different_clients,
            "#7C3AED",
        )

        self._view._top_3_spenders.controls.clear()
        self._view._top_3_spenders.controls.extend(
            self._header(
                "Clienti con spesa maggiore",
                ft.icons.PAID,
                "Top 3 clienti per valore acquistato",
            )
        )
        spenders = [f"{client[0]} {client[1]}" for client in top_3_spenders]
        self._add_ranked_items(self._view._top_3_spenders, spenders, "#DB2777")

        self._view.update_page()

    def handle_graph1(self, e):
        self._view._lv_graph1.controls.clear()
        self._view._lv_algo_graph1.controls.clear()

        data1 = self._view._data_graph1_1.value
        data2 = self._view._data_graph1_2.value
        genre = self._view._dd_genres.value

        if data1 is None or data2 is None or genre is None:
            self._view._lv_graph1.controls.append(
                self._view.create_message("Seleziona le date e un genere per proseguire.", "error")
            )
            self._view.update_page()
            return

        if data1 > data2:
            self._view._lv_graph1.controls.append(
                self._view.create_message("Seleziona un intervallo di date esistente.", "error")
            )
            self._view.update_page()
            return

        self._view._lv_graph1.controls.append(
            self._view.create_message(
                f"Intervallo selezionato: {data1} - {data2} | Genere: {genre}",
                "info",
            )
        )

        self._model.buildGraph1(genre, data1, data2)
        if len(list(self._model._graph1.nodes)) == 0:
            self._view._lv_graph1.controls.append(
                self._view.create_message(
                    f"Con questi parametri il grafo ha zero nodi.\n"
                    "Si consiglia di scegleire un intervallo temporale tra il 2020 e 2026",
                )
            )
            self._view.update_page()
            return
        self.fill_ddTracks_graph1()
        self._view._btn_algo_graph1.disabled = False

        self._view._lv_graph1.controls.append(
            self._view.create_message(
                f"Grafo correttamente creato. {self._model.printGraph1()}",
                "success",
            )
        )
        top_bridge_tracks = self._model.get_top_bridge_tracks()

        self._view._lv_graph1.controls.append(
            self._view.create_result_card(
                "Top 3 brani piu centrali",
                "Betweenness Centrality ---> nodi più centrali nel grafo.",
                "#0F766E",
            )
        )

        for i, item in enumerate(top_bridge_tracks, start=1):
            self._view._lv_graph1.controls.append(
                self._view.create_result_card(
                    f"{i}. {item['track']}",
                    [
                        f"Grado: {item['degree']}",
                        f"Grado pesato: {item['weighted_degree']}",
                        f"Centralita: {item['centrality']:.4f}",
                    ],
                    "#0F766E",
                )
            )

        self._view.update_page()

    def handle_optPath_graph1(self, e):
        self._view._lv_algo_graph1.controls.clear()

        track_id = self._view._dd_track_graph1.value
        k = self._view._dd_k_graph1.value

        if track_id is None or k is None:
            self._view._lv_algo_graph1.controls.append(
                self._view.create_message("Seleziona un brano di partenza e un valore di k.", "error")
            )
            self._view.update_page()
            return

        track_id = int(track_id)
        k = int(k)

        soluzione, score = self._model.get_optPath_coAcquisto(track_id, k)
        track_start = self._model._idMapNodes_1[track_id]

        self._view._lv_algo_graph1.controls.append(
            self._view.create_result_card(
                "Percorso ottimo calcolato",
                [
                    f"Brano di partenza: {track_start.Name}",
                    f"K brani: {k}",
                    f"Score: {score}",
                ],
                "#0F766E",
            )
        )

        for i, track in enumerate(soluzione, start=1):
            self._view._lv_algo_graph1.controls.append(
                self._view.create_rank_item(i, track, "#0F766E")
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

    def handle_graph2(self, e):
        self._view._lv_graph2.controls.clear()
        self._view._lv_algo_graph2.controls.clear()

        data1 = self._view._data_graph2_1.value
        data2 = self._view._data_graph2_2.value
        soglia = self._view._dd_soglia_graph2.value

        if data1 is None or data2 is None or soglia is None:
            self._view._lv_graph2.controls.append(
                self._view.create_message("Seleziona le date e una soglia per proseguire.", "error")
            )
            self._view.update_page()
            return

        if data1 > data2:
            self._view._lv_graph2.controls.append(
                self._view.create_message("Seleziona un intervallo di date esistente.", "error")
            )
            self._view.update_page()
            return

        self._view._lv_graph2.controls.append(
            self._view.create_message(
                f"Intervallo selezionato: {data1} - {data2} | Soglia: {soglia}",
                "info",
            )
        )
        soglia = int(soglia)

        self._model.buildGraph2(soglia, data1, data2)
        if len(list(self._model._graph2.nodes)) == 0:
            self._view._lv_graph2.controls.append(
                self._view.create_message(
                    f"Con questi parametri il grafo ha zero nodi.\n"
                    "Si consiglia di scegleire un intervallo temporale tra il 2020 e 2026",
                )
            )
            self._view.update_page()
            return
        self._view._btn_algo_graph2.disabled = False
        self._view._lv_graph2.controls.append(
            self._view.create_message(
                f"Grafo correttamente creato. {self._model.printGraph2()}",
                "success",
            )
        )
        top_artists = self._model.get_top_artists()

        self._view._lv_graph2.controls.append(
            self._view.create_result_card("Top 3 artisti piu centrali", "Centralita sul grafo artisti", "#2563EB")
        )

        for i, (artist, degree, weighted_degree, centrality) in enumerate(top_artists, start=1):
            self._view._lv_graph2.controls.append(
                self._view.create_result_card(
                    f"{i}. {artist}",
                    [
                        f"Grado: {degree}",
                        f"Grado pesato: {weighted_degree}",
                        f"Centralita: {centrality:.4f}",
                    ],
                    "#2563EB",
                )
            )
        self._view.update_page()

    def handle_optPath_graph2(self, e):
        self._view._lv_algo_graph2.controls.clear()

        k_artisti = self._view._dd_k_artisti_graph2.value
        alfa = self._view._dd_alfa_graph2.value

        if k_artisti is None or alfa is None:
            self._view._lv_algo_graph2.controls.append(
                self._view.create_message("Seleziona il numero di artisti e il valore di alfa.", "error")
            )
            self._view.update_page()
            return

        k_artisti = int(k_artisti)
        alfa = float(alfa)

        best_artists, best_score = self._model.get_optPath_Artisti(k_artisti, alfa)

        self._view._lv_algo_graph2.controls.append(
            self._view.create_result_card(
                "Funzione di score utilizzata",
                "score = clienti_coperti - alfa * sovrapposizione",
                "#2563EB",
            )
        )

        self._view._lv_algo_graph2.controls.append(
            self._view.create_result_card(
                "Parametri selezionati",
                [
                    f"Numero artisti: {k_artisti}",
                    f"Alfa: {alfa}",
                    f"Score migliore ottenuto: {best_score:.2f}",
                ],
                "#2563EB",
            )
        )

        self._view._lv_algo_graph2.controls.append(
            self._view.create_result_card("Artisti selezionati", "Risultato dell'ottimizzazione", "#2563EB")
        )

        for i, artist in enumerate(best_artists, start=1):
            self._view._lv_algo_graph2.controls.append(
                self._view.create_rank_item(i, artist, "#2563EB")
            )
        self._view.update_page()

    ### parte grafo 3 #####

    def handle_graph3(self, e):
        self._view._lv_graph3.controls.clear()
        self._view._lv_algo_graph3.controls.clear()

        soglia = self._view._dd_soglia_graph3.value

        if soglia is None:
            self._view._lv_graph3.controls.append(
                self._view.create_message("Seleziona una soglia per proseguire.", "error")
            )
            self._view.update_page()
            return

        soglia = int(soglia)

        self._view._lv_graph3.controls.append(
            self._view.create_message(f"Soglia selezionata: {soglia}", "info")
        )

        self._model.buildGraph3(soglia)
        if len(list(self._model._graph3.nodes)) == 0:
            self._view._lv_graph3.controls.append(
                self._view.create_message(
                    f"Con questi parametri il grafo ha zero nodi.\n"

                )
            )
            self._view.update_page()
            return
        self._view._btn_algo_graph3.disabled = False

        self._view._lv_graph3.controls.append(
            self._view.create_message(
                f"Grafo correttamente creato. {self._model.printGraph3()}",
                "success",
            )
        )

        representative_customers, outlier_customers = self._model.analyze_customer_segments()

        self._view._lv_graph3.controls.append(
            self._view.create_result_card("Top 3 clienti piu rappresentativi", "Clienti con maggiore connessione", "#F59E0B")
        )

        for i, customer_data in enumerate(representative_customers, start=1):
            customer = customer_data["customer"]

            self._view._lv_graph3.controls.append(
                self._view.create_result_card(
                    f"{i}. {customer}",
                    [
                        f"Grado: {customer_data['degree']}",
                        f"Grado pesato: {customer_data['weighted_degree']}",
                    ],
                    "#F59E0B",
                )
            )

        self._view._lv_graph3.controls.append(
            self._view.create_result_card("Clienti outlier", "Clienti poco collegati al resto del grafo", "#DB2777")
        )

        if len(outlier_customers) == 0:
            self._view._lv_graph3.controls.append(
                self._view.create_message("Nessun outlier individuato.", "success")
            )
        else:
            for customer_data in outlier_customers:
                customer = customer_data["customer"]

                self._view._lv_graph3.controls.append(
                    self._view.create_result_card(
                        str(customer),
                        [
                            f"Grado: {customer_data['degree']}",
                            f"Grado pesato: {customer_data['weighted_degree']}",
                        ],
                        "#DB2777",
                    )
                )

        self._view.update_page()

    def handle_optPath_graph3(self, e):
        self._view._lv_algo_graph3.controls.clear()

        k_clienti = self._view._dd_k_clienti_graph3.value
        alfa = self._view._dd_alfa_graph3.value

        if k_clienti is None or alfa is None:
            self._view._lv_algo_graph3.controls.append(
                self._view.create_message("Seleziona il numero di clienti e il valore di alfa.", "error")
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
            self._view.create_result_card(
                "Funzione di score utilizzata",
                "score = copertura - alfa * sovrapposizione",
                "#F59E0B",
            )
        )

        self._view._lv_algo_graph3.controls.append(
            self._view.create_result_card(
                "Parametri selezionati",
                [
                    f"Numero clienti selezionato: {k_clienti}",
                    f"Alfa: {alfa}",
                    f"Score migliore ottenuto: {best_score:.2f}",
                ],
                "#F59E0B",
            )
        )

        self._view._lv_algo_graph3.controls.append(
            self._view.create_result_card("Clienti selezionati", "Risultato dell'ottimizzazione", "#F59E0B")
        )

        for i, customer in enumerate(best_clients, start=1):
            self._view._lv_algo_graph3.controls.append(
                self._view.create_rank_item(i, customer, "#F59E0B")
            )

        self._view.update_page()
