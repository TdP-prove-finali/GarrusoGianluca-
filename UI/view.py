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
