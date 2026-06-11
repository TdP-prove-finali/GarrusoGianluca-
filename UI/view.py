from datetime import datetime

import flet as ft


class View(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page
        self._page.title = "Applicazione di analisi musicale"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"

        self.spacing = 20
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self._controller = None

    def load_interface(self):
        self._page.scroll = ft.ScrollMode.AUTO
        self._title = ft.Text("Applicazione di analisi musicale", color="green", size=24)
        self._page.controls.append(self._title)

        self._subtitle = ft.Text("Analisi insight", color="green", size=20)
        self._page.controls.append(self._subtitle)

        self._top_tracks_col = ft.Column()
        self._top_artists_col = ft.Column()
        self._top_genres_col = ft.Column()

        self._row_top = ft.Row(
            controls=[
                ft.Container(
                    content=self._top_tracks_col,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
                ft.Container(
                    content=self._top_artists_col,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
                ft.Container(
                    content=self._top_genres_col,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        self._page.controls.append(self._row_top)

        #row statistiche
        self._num_clienti = ft.Column()
        self._num_fatture = ft.Column()
        self._num_tracce = ft.Column()
        self._row_statistiche = ft.Row(
            controls=[
                ft.Container(
                    content=self._num_clienti,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
                ft.Container(
                    content=self._num_fatture,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
                ft.Container(
                    content=self._num_tracce,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        self._top_3_artist_with_more_different_client = ft.Column()
        self._top_3_spenders = ft.Column()
        self._row_top3 = ft.Row(
            controls=[
                ft.Container(
                    content=self._top_3_artist_with_more_different_client,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
                ft.Container(
                    content=self._top_3_spenders,
                    width=200,
                    padding=10,
                    border=ft.border.all(1)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self._page.controls.append(self._row_statistiche)
        self._page.controls.append(self._row_top3)
        self._controller.fill_insights()


        # Parte Grafo 1

        self._data_graph1_1 = ft.DatePicker(
            value=datetime(2020, 1, 1)
        )
        self._page.overlay.append(self._data_graph1_1)

        self._data_graph1_2 = ft.DatePicker(
            value=datetime(2025, 1, 1)
        )
        self._page.overlay.append(self._data_graph1_2)

        self._btn_date1_graph1 = ft.ElevatedButton(
            "Data inizio",
            on_click=lambda e: self._page.open(self._data_graph1_1)
        )

        self._btn_date2_graph1 = ft.ElevatedButton(
            "Data fine",
            on_click=lambda e: self._page.open(self._data_graph1_2)
        )

        self._dd_genres = ft.Dropdown(
            label="Genere",
            width=200
        )

        self._controller.fill_ddGenres()

        self._btn_graph1 = ft.ElevatedButton(
            "Crea Grafo 1",
            on_click=self._controller.handle_graph1
        )


        self._lv_graph1 = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False
        )

        self._graph1_section = ft.Column(
            controls=[
                ft.Text("Grafo 1 - Co-acquisto brani", size=18, weight=ft.FontWeight.BOLD),

                ft.Row(
                    controls=[
                        self._btn_date1_graph1,
                        self._btn_date2_graph1,
                        self._dd_genres,
                        self._btn_graph1
                    ],
                    spacing=20
                ),

                ft.Container(
                    content=self._lv_graph1,
                    height=300,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=10
                )
            ],
            spacing=15
        )

        self._page.add(self._graph1_section)

        #sezione algoritmica grafo 1
        self._dd_track_graph1 = ft.Dropdown(
            label="Brano di partenza",
            width=350
        )

        self._dd_k_graph1 = ft.Dropdown(
            label="Numero brani",
            width=150,
            options=[
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
                ft.dropdown.Option("6")
            ]
        )

        self._btn_algo_graph1 = ft.ElevatedButton(
            "Calcola percorso ottimo",
            on_click=self._controller.handle_optPath_graph1,
            disabled=True
        )

        self._lv_algo_graph1 = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False
        )

        self._graph1_algo_section = ft.Column(
            controls=[
                ft.Text("Algoritmi Grafo 1", size=18, weight=ft.FontWeight.BOLD),

                ft.Row(
                    controls=[
                        self._dd_track_graph1,
                        self._dd_k_graph1,
                        self._btn_algo_graph1
                    ],
                    spacing=20
                ),

                ft.Container(
                    content=self._lv_algo_graph1,
                    height=250,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=10
                )
            ],
            spacing=15
        )
        self._page.add(self._graph1_algo_section)

        #####  SEZIONE GRAFO 2    #####
        # Parte Grafo 2

        self._data_graph2_1 = ft.DatePicker(
            value=datetime(2020, 1, 1)
        )
        self._page.overlay.append(self._data_graph2_1)

        self._data_graph2_2 = ft.DatePicker(
            value=datetime(2025, 1, 1)
        )
        self._page.overlay.append(self._data_graph2_2)

        self._btn_date1_graph2 = ft.ElevatedButton(
            "Data inizio",
            on_click=lambda e: self._page.open(self._data_graph2_1)
        )

        self._btn_date2_graph2 = ft.ElevatedButton(
            "Data fine",
            on_click=lambda e: self._page.open(self._data_graph2_2)
        )

        self._dd_soglia_graph2 = ft.Dropdown(
            label="Soglia clienti",
            width=180,
            options=[
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5")
            ]
        )

        self._btn_graph2 = ft.ElevatedButton(
            "Crea Grafo 2",
            on_click=self._controller.handle_graph2
        )

        self._lv_graph2 = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False
        )

        self._graph2_section = ft.Column(
            controls=[
                ft.Text("Grafo 2 - Artisti con clienti condivisi", size=18, weight=ft.FontWeight.BOLD),

                ft.Row(
                    controls=[
                        self._btn_date1_graph2,
                        self._btn_date2_graph2,
                        self._dd_soglia_graph2,
                        self._btn_graph2
                    ],
                    spacing=20
                ),

                ft.Container(
                    content=self._lv_graph2,
                    height=300,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=10
                )
            ],
            spacing=15
        )
        self._page.add(self._graph2_section)

        # Parte Algoritmi Grafo 2

        self._dd_k_artisti_graph2 = ft.Dropdown(
            label="Numero artisti",
            width=180,
            options=[
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3")
            ]
        )

        self._dd_alfa_graph2 = ft.Dropdown(
            label="Alfa",
            width=150,
            options=[
                ft.dropdown.Option("0.25"),
                ft.dropdown.Option("0.5"),
                ft.dropdown.Option("0.75"),
                ft.dropdown.Option("1")
            ]
        )

        self._btn_algo_graph2 = ft.ElevatedButton(
            "Calcola artisti ottimali",
            on_click=self._controller.handle_optPath_graph2,
            disabled=True
        )

        self._lv_algo_graph2 = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False
        )

        self._graph2_algo_section = ft.Column(
            controls=[
                ft.Text(
                    "Algoritmi Grafo 2",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Selezione degli artisti migliori considerando clienti coperti e sovrapposizione."
                ),

                ft.Row(
                    controls=[
                        self._dd_k_artisti_graph2,
                        self._dd_alfa_graph2,
                        self._btn_algo_graph2
                    ],
                    spacing=20
                ),

                ft.Container(
                    content=self._lv_algo_graph2,
                    height=250,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=10
                )
            ],
            spacing=15
        )
        self._page.add(self._graph2_algo_section)

        ###### Parte Grafo 3 ########

        self._dd_soglia_graph3 = ft.Dropdown(
            label="Soglia similarità",
            width=180,
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4")
            ]
        )

        self._btn_graph3 = ft.ElevatedButton(
            "Crea Grafo 3",
            on_click=self._controller.handle_graph3
        )

        self._lv_graph3 = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False
        )

        self._graph3_section = ft.Column(
            controls=[
                ft.Text(
                    "Grafo 3 - Clienti simili",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    controls=[
                        self._dd_soglia_graph3,
                        self._btn_graph3
                    ],
                    spacing=20
                ),

                ft.Container(
                    content=self._lv_graph3,
                    height=300,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=10
                )
            ],
            spacing=15
        )
        self._page.add(self._graph3_section)

        #### Parte Algoritmi Grafo 3 ####

        self._dd_k_clienti_graph3 = ft.Dropdown(
            label="Numero clienti",
            width=180,
            options=[
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4")
            ]
        )

        self._dd_alfa_graph3 = ft.Dropdown(
            label="Alfa",
            width=150,
            options=[
                ft.dropdown.Option("0.25"),
                ft.dropdown.Option("0.5"),
                ft.dropdown.Option("0.75"),
                ft.dropdown.Option("1")
            ]
        )

        self._btn_algo_graph3 = ft.ElevatedButton(
            "Calcola clienti ottimali",
            on_click=self._controller.handle_optPath_graph3,
            disabled = True
        )

        self._lv_algo_graph3 = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False
        )

        self._graph3_algo_section = ft.Column(
            controls=[
                ft.Text(
                    "Algoritmi Grafo 3",
                    size=18,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Selezione dei clienti migliori considerando copertura e sovrapposizione."
                ),

                ft.Row(
                    controls=[
                        self._dd_k_clienti_graph3,
                        self._dd_alfa_graph3,
                        self._btn_algo_graph3
                    ],
                    spacing=20
                ),

                ft.Container(
                    content=self._lv_algo_graph3,
                    height=250,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=10
                )
            ],
            spacing=15
        )
        self._page.add(self._graph3_algo_section)


        self._page.update()





    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()
