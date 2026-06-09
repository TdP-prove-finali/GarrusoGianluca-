import flet as ft


class Controller:
    def __init__(self, view, model):
        # La view contiene gli elementi grafici dell'interfaccia
        self._view = view
        # Il model contiene la logica applicativa e i dati
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
        self._view.update_page()

        self._model.buildGraph1(genre,data1, data2)

        self._view._lv_graph1.controls.append(
            ft.Text(
                f"Grafo correttamente creato\n"
                f"{self._model.printGraph1()}"
            )
        )
        self._view.update_page()




    def fill_ddGenres(self):
        genres = self._model.get_name_genres()

        self._view._dd_genres.options.clear()

        for genre in genres:
            self._view._dd_genres.options.append(
                ft.dropdown.Option(genre)
            )










