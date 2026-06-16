from datetime import datetime

import flet as ft


PRIMARY = "#0F766E"
PRIMARY_DARK = "#115E59"
ACCENT = "#F59E0B"
INK = "#0F172A"
MUTED = "#64748B"
LINE = "#D7E3E4"
SURFACE = "#FFFFFF"
SOFT = "#F6FAFA"
SUCCESS_BG = "#ECFDF5"
SUCCESS_TEXT = "#047857"
ERROR_BG = "#FEF2F2"
ERROR_TEXT = "#B91C1C"


class View(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page
        self._page.title = "Applicazione di analisi musicale"
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#EAF3F2"
        self._page.padding = 0
        self._page.window_min_width = 960
        self._page.window_min_height = 720

        self.spacing = 0
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self._controller = None

    def _text(self, value, size=14, color=INK, weight=None):
        return ft.Text(
            value,
            size=size,
            color=color,
            weight=weight,
            selectable=True,
        )

    def _input_button_style(self):
        return ft.ButtonStyle(
            bgcolor=SURFACE,
            color=PRIMARY_DARK,
            elevation=0,
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, LINE),
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
        )

    def _primary_button_style(self):
        return ft.ButtonStyle(
            bgcolor=PRIMARY,
            color=ft.colors.WHITE,
            elevation=1,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=18, vertical=14),
        )

    def _style_dropdown(self, dropdown):
        dropdown.border_color = LINE
        dropdown.focused_border_color = PRIMARY
        dropdown.border_radius = 8
        dropdown.filled = True
        dropdown.bgcolor = SURFACE
        dropdown.color = INK
        dropdown.label_style = ft.TextStyle(color=MUTED)
        return dropdown

    def _section_title(self, title, subtitle=None, icon=ft.icons.INSIGHTS):
        controls = [
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=PRIMARY_DARK, size=22),
                        width=42,
                        height=42,
                        alignment=ft.alignment.center,
                        bgcolor="#DDF4EF",
                        border_radius=8,
                    ),
                    ft.Column(
                        controls=[
                            self._text(title, size=20, color=INK, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
        if subtitle is not None:
            controls[0].controls[1].controls.append(self._text(subtitle, size=13, color=MUTED))
        return controls[0]

    def _card(self, content, padding=18, width=None, expand=False):
        return ft.Container(
            content=content,
            padding=padding,
            bgcolor=SURFACE,
            border_radius=8,
            border=ft.border.all(1, LINE),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=16,
                color="#1E3A3A14",
                offset=ft.Offset(0, 4),
            ),
            width=width,
            expand=expand,
        )

    def _output_box(self, list_view, height=280):
        return ft.Container(
            content=list_view,
            height=height,
            padding=12,
            bgcolor="#FBFEFE",
            border=ft.border.all(1, LINE),
            border_radius=8,
        )

    def _controls_row(self, controls):
        return ft.Row(
            controls=controls,
            spacing=12,
            run_spacing=12,
            wrap=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _graph_section(self, title, subtitle, icon, controls, list_view, height=300):
        return self._card(
            ft.Column(
                controls=[
                    self._section_title(title, subtitle, icon),
                    self._controls_row(controls),
                    self._output_box(list_view, height),
                ],
                spacing=16,
            ),
            padding=20,
        )

    def create_rank_item(self, index, text, accent=PRIMARY):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(str(index), color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                        width=28,
                        height=28,
                        alignment=ft.alignment.center,
                        bgcolor=accent,
                        border_radius=8,
                    ),
                    ft.Text(str(text), size=13, color=INK, expand=True, selectable=True),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=10,
            bgcolor="#F8FCFC",
            border=ft.border.all(1, "#E4EEEE"),
            border_radius=8,
        )

    def create_metric_value(self, label, value, icon, accent=PRIMARY):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, color=accent, size=22),
                        ft.Text(label, color=MUTED, size=13, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(str(value), color=INK, size=30, weight=ft.FontWeight.BOLD),
            ],
            spacing=8,
        )

    def create_message(self, text, kind="info"):
        color = PRIMARY_DARK
        bgcolor = "#EAF7F5"
        icon = ft.icons.INFO_OUTLINE
        if kind == "error":
            color = ERROR_TEXT
            bgcolor = ERROR_BG
            icon = ft.icons.ERROR_OUTLINE
        elif kind == "success":
            color = SUCCESS_TEXT
            bgcolor = SUCCESS_BG
            icon = ft.icons.CHECK_CIRCLE_OUTLINE

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(text, color=color, size=13, expand=True, selectable=True),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=12,
            bgcolor=bgcolor,
            border_radius=8,
            border=ft.border.all(1, f"{color}22"),
        )

    def create_result_card(self, title, lines, accent=PRIMARY):
        if isinstance(lines, str):
            lines = [lines]
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(width=4, height=26, bgcolor=accent, border_radius=4),
                            ft.Text(title, size=14, color=INK, weight=ft.FontWeight.BOLD, expand=True, selectable=True),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    *[ft.Text(str(line), size=13, color=INK, selectable=True) for line in lines],
                ],
                spacing=6,
            ),
            padding=12,
            bgcolor=SURFACE,
            border=ft.border.all(1, "#E1ECEC"),
            border_radius=8,
        )

    def load_interface(self):
        self._page.scroll = ft.ScrollMode.AUTO

        self._title = ft.Text(
            "Applicazione di analisi musicale",
            color=ft.colors.WHITE,
            size=30,
            weight=ft.FontWeight.BOLD,
            selectable=True,
        )
        self._subtitle = ft.Text(
            "Dashboard per insight, grafi e percorsi ottimi sul database musicale.",
            color="#DDF4EF",
            size=14,
            selectable=True,
        )

        header = ft.Container(
            content=ft.Column(
                controls=[
                    self._title,
                    self._subtitle,
                ],
                spacing=6,
            ),
            padding=ft.padding.symmetric(horizontal=36, vertical=28),
            bgcolor=PRIMARY_DARK,
            width=1100,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        )

        content = ft.Column(
            controls=[header],
            width=1100,
            spacing=22,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self._top_tracks_col = ft.Column(spacing=8)
        self._top_artists_col = ft.Column(spacing=8)
        self._top_genres_col = ft.Column(spacing=8)

        self._row_top = ft.Row(
            controls=[
                self._card(self._top_tracks_col, width=318),
                self._card(self._top_artists_col, width=318),
                self._card(self._top_genres_col, width=318),
            ],
            spacing=14,
            run_spacing=14,
            wrap=True,
            tight=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self._num_clienti = ft.Column(spacing=8)
        self._num_fatture = ft.Column(spacing=8)
        self._num_tracce = ft.Column(spacing=8)
        self._row_statistiche = ft.Row(
            controls=[
                self._card(self._num_clienti, width=318),
                self._card(self._num_fatture, width=318),
                self._card(self._num_tracce, width=318),
            ],
            spacing=14,
            run_spacing=14,
            wrap=True,
            tight=True,
        )

        self._top_3_artist_with_more_different_client = ft.Column(spacing=8)
        self._top_3_spenders = ft.Column(spacing=8)
        self._row_top3 = ft.Row(
            controls=[
                self._card(self._top_3_artist_with_more_different_client, width=489),
                self._card(self._top_3_spenders, width=489),
            ],
            spacing=14,
            run_spacing=14,
            wrap=True,
            tight=True,
        )

        insights = ft.Container(
            content=ft.Column(
                controls=[
                    self._section_title(
                        "Insight principali",
                        "Una lettura rapida dei contenuti piu rilevanti del catalogo e dei clienti.",
                        ft.icons.AUTO_GRAPH,
                    ),
                    self._row_statistiche,
                    self._row_top,
                    self._row_top3,
                ],
                spacing=16,
            ),
            padding=ft.padding.symmetric(horizontal=36, vertical=8),
        )
        content.controls.append(insights)

        self._controller.fill_insights()

        self._data_graph1_1 = ft.DatePicker(value=datetime(2020, 1, 1))
        self._page.overlay.append(self._data_graph1_1)
        self._data_graph1_2 = ft.DatePicker(value=datetime(2025, 1, 1))
        self._page.overlay.append(self._data_graph1_2)
        self._btn_date1_graph1 = ft.ElevatedButton(
            "Data inizio",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self._page.open(self._data_graph1_1),
            style=self._input_button_style(),
        )
        self._btn_date2_graph1 = ft.ElevatedButton(
            "Data fine",
            icon=ft.icons.EVENT,
            on_click=lambda e: self._page.open(self._data_graph1_2),
            style=self._input_button_style(),
        )
        self._dd_genres = self._style_dropdown(ft.Dropdown(label="Genere", width=220))
        self._controller.fill_ddGenres()
        self._btn_graph1 = ft.ElevatedButton(
            "Crea Grafo 1",
            icon=ft.icons.ACCOUNT_TREE,
            on_click=self._controller.handle_graph1,
            style=self._primary_button_style(),
        )
        self._lv_graph1 = ft.ListView(expand=True, spacing=10, auto_scroll=False)
        self._graph1_section = self._graph_section(
            "Grafo 1 - Co-acquisto brani",
            "Analizza la correlazione tra 2 brani acquistati nella stessa ricevuta",
            ft.icons.GRAPHIC_EQ,
            [self._btn_date1_graph1, self._btn_date2_graph1, self._dd_genres, self._btn_graph1],
            self._lv_graph1,
            300,
        )
        content.controls.append(ft.Container(self._graph1_section, padding=ft.padding.symmetric(horizontal=36)))

        self._dd_track_graph1 = self._style_dropdown(ft.Dropdown(label="Brano di partenza", width=360))
        self._dd_k_graph1 = self._style_dropdown(
            ft.Dropdown(
                label="Numero brani",
                width=160,
                options=[ft.dropdown.Option(str(i)) for i in range(2, 7)],
            )
        )
        self._btn_algo_graph1 = ft.ElevatedButton(
            "Calcola percorso ottimo",
            icon=ft.icons.ROUTE,
            on_click=self._controller.handle_optPath_graph1,
            disabled=True,
            style=self._primary_button_style(),
        )
        self._lv_algo_graph1 = ft.ListView(expand=True, spacing=10, auto_scroll=False)
        self._graph1_algo_section = self._graph_section(
            "Algoritmi Grafo 1",
            "Trova una sequenza di brani con il miglior score di co-acquisto.",
            ft.icons.ROUTE,
            [self._dd_track_graph1, self._dd_k_graph1, self._btn_algo_graph1],
            self._lv_algo_graph1,
            250,
        )
        content.controls.append(ft.Container(self._graph1_algo_section, padding=ft.padding.symmetric(horizontal=36)))

        self._data_graph2_1 = ft.DatePicker(value=datetime(2020, 1, 1))
        self._page.overlay.append(self._data_graph2_1)
        self._data_graph2_2 = ft.DatePicker(value=datetime(2025, 1, 1))
        self._page.overlay.append(self._data_graph2_2)
        self._btn_date1_graph2 = ft.ElevatedButton(
            "Data inizio",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self._page.open(self._data_graph2_1),
            style=self._input_button_style(),
        )
        self._btn_date2_graph2 = ft.ElevatedButton(
            "Data fine",
            icon=ft.icons.EVENT,
            on_click=lambda e: self._page.open(self._data_graph2_2),
            style=self._input_button_style(),
        )
        self._dd_soglia_graph2 = self._style_dropdown(
            ft.Dropdown(
                label="Soglia clienti",
                width=180,
                options=[ft.dropdown.Option(str(i)) for i in range(2, 6)],
            )
        )
        self._btn_graph2 = ft.ElevatedButton(
            "Crea Grafo 2",
            icon=ft.icons.HUB,
            on_click=self._controller.handle_graph2,
            style=self._primary_button_style(),
        )
        self._lv_graph2 = ft.ListView(expand=True, spacing=10, auto_scroll=False)
        self._graph2_section = self._graph_section(
            "Grafo 2 - Artisti con clienti condivisi",
            "Collega gli artisti quando condividono clienti oltre la soglia selezionata.",
            ft.icons.GROUPS,
            [self._btn_date1_graph2, self._btn_date2_graph2, self._dd_soglia_graph2, self._btn_graph2],
            self._lv_graph2,
            300,
        )
        content.controls.append(ft.Container(self._graph2_section, padding=ft.padding.symmetric(horizontal=36)))

        self._dd_k_artisti_graph2 = self._style_dropdown(
            ft.Dropdown(
                label="Numero artisti",
                width=180,
                options=[ft.dropdown.Option("2"), ft.dropdown.Option("3")],
            )
        )
        self._dd_alfa_graph2 = self._style_dropdown(
            ft.Dropdown(
                label="Alfa",
                width=150,
                options=[ft.dropdown.Option(v) for v in ["0.25", "0.5", "0.75", "1"]],
            )
        )
        self._btn_algo_graph2 = ft.ElevatedButton(
            "Calcola artisti ottimali",
            icon=ft.icons.EMOJI_EVENTS,
            on_click=self._controller.handle_optPath_graph2,
            disabled=True,
            style=self._primary_button_style(),
        )
        self._lv_algo_graph2 = ft.ListView(expand=True, spacing=10, auto_scroll=False)
        self._graph2_algo_section = self._graph_section(
            "Algoritmi Grafo 2",
            "Selezione degli artisti migliori considerando clienti coperti e sovrapposizione.",
            ft.icons.EMOJI_EVENTS,
            [self._dd_k_artisti_graph2, self._dd_alfa_graph2, self._btn_algo_graph2],
            self._lv_algo_graph2,
            250,
        )
        content.controls.append(ft.Container(self._graph2_algo_section, padding=ft.padding.symmetric(horizontal=36)))

        self._dd_soglia_graph3 = self._style_dropdown(
            ft.Dropdown(
                label="Soglia similarita",
                width=190,
                options=[ft.dropdown.Option(str(i)) for i in range(1, 5)],
            )
        )
        self._btn_graph3 = ft.ElevatedButton(
            "Crea Grafo 3",
            icon=ft.icons.DIVERSITY_3,
            on_click=self._controller.handle_graph3,
            style=self._primary_button_style(),
        )
        self._lv_graph3 = ft.ListView(expand=True, spacing=10, auto_scroll=False)
        self._graph3_section = self._graph_section(
            "Grafo 3 - Clienti simili",
            "Individua clienti vicini per comportamento di acquisto.",
            ft.icons.DIVERSITY_3,
            [self._dd_soglia_graph3, self._btn_graph3],
            self._lv_graph3,
            300,
        )
        content.controls.append(ft.Container(self._graph3_section, padding=ft.padding.symmetric(horizontal=36)))

        self._dd_k_clienti_graph3 = self._style_dropdown(
            ft.Dropdown(
                label="Numero clienti",
                width=180,
                options=[ft.dropdown.Option(str(i)) for i in range(2, 5)],
            )
        )
        self._dd_alfa_graph3 = self._style_dropdown(
            ft.Dropdown(
                label="Alfa",
                width=150,
                options=[ft.dropdown.Option(v) for v in ["0.25", "0.5", "0.75", "1"]],
            )
        )
        self._btn_algo_graph3 = ft.ElevatedButton(
            "Calcola clienti ottimali",
            icon=ft.icons.STAR_RATE,
            on_click=self._controller.handle_optPath_graph3,
            disabled=True,
            style=self._primary_button_style(),
        )
        self._lv_algo_graph3 = ft.ListView(expand=True, spacing=10, auto_scroll=False)
        self._graph3_algo_section = self._graph_section(
            "Algoritmi Grafo 3",
            "Selezione dei clienti migliori considerando copertura e sovrapposizione.",
            ft.icons.STAR_RATE,
            [self._dd_k_clienti_graph3, self._dd_alfa_graph3, self._btn_algo_graph3],
            self._lv_algo_graph3,
            250,
        )
        content.controls.append(ft.Container(self._graph3_algo_section, padding=ft.padding.only(left=36, right=36, bottom=36)))

        self._page.controls.append(content)
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
