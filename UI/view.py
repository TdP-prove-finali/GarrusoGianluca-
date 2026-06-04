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

        # Elementi grafici principali
        self._title = None
        self._subtitle = None

        # Card lista
        self._card_top_brani = None
        self._lista_top_brani = None

        self._card_top_artisti = None
        self._lista_top_artisti = None

        self._card_top_generi = None
        self._lista_top_generi = None

        self._card_top_clienti_spesa = None
        self._lista_top_clienti_spesa = None

        self._card_top_artisti_clienti = None
        self._lista_top_artisti_clienti = None

        # Card numeriche
        self._txt_num_clienti = None
        self._txt_num_fatture = None
        self._txt_num_tracce = None

    def load_interface(self):
        """Costruisce la schermata principale dell'applicazione."""

        self._title = ft.Text(
            "Applicazione di analisi musicale",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="#1f3b4d",
            text_align=ft.TextAlign.CENTER
        )

        self._subtitle = ft.Text(
            "Dashboard iniziale e analisi dei grafi",
            size=15,
            color="#52616b",
            text_align=ft.TextAlign.CENTER
        )

        titolo_insights = ft.Text(
            "📊 Insights del database",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#1f3b4d"
        )

        # Prima riga: classifiche principali
        self._card_top_brani, self._lista_top_brani = self._crea_card_lista("🎵 Top 5 brani venduti")
        self._card_top_artisti, self._lista_top_artisti = self._crea_card_lista("🎤 Top 5 artisti più venduti")
        self._card_top_generi, self._lista_top_generi = self._crea_card_lista("💿 Top 5 generi più venduti")

        row_top = ft.Row(
            controls=[
                self._card_top_brani,
                self._card_top_artisti,
                self._card_top_generi
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True
        )

        # Seconda riga: numeri generali
        card_clienti, self._txt_num_clienti = self._crea_card_numero("Clienti", "👥")
        card_fatture, self._txt_num_fatture = self._crea_card_numero("Fatture", "🧾")
        card_tracce, self._txt_num_tracce = self._crea_card_numero("Tracce", "🎼")

        row_numeri = ft.Row(
            controls=[
                card_clienti,
                card_fatture,
                card_tracce
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True
        )

        # Terza riga: insight avanzati
        self._card_top_clienti_spesa, self._lista_top_clienti_spesa = self._crea_card_lista(
            "💰 Top 3 clienti per spesa",
            width=460
        )
        self._card_top_artisti_clienti, self._lista_top_artisti_clienti = self._crea_card_lista(
            "🌐 Top 3 artisti per clienti distinti",
            width=460
        )

        row_extra = ft.Row(
            controls=[
                self._card_top_clienti_spesa,
                self._card_top_artisti_clienti
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            wrap=True
        )

        insights_section = ft.Container(
            content=ft.Column(
                controls=[
                    titolo_insights,
                    row_top,
                    row_numeri,
                    row_extra
                ],
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=25,
            bgcolor="#dff0f2",
            border_radius=20,
            width=1100
        )
        self._txt_data_inizio = ft.TextField(label="Data inizio", hint_text="2021-01-01", width=180)
        self._txt_data_fine = ft.TextField(label="Data fine", hint_text="2023-01-01", width=180)

        self._dd_genere = ft.Dropdown(
            label="Genere",
            width=220,
            options=[]
        )

        self._btn_crea_grafo1 = ft.ElevatedButton(
            text="Crea Grafo 1",
            on_click=lambda e: self._controller.handle_crea_grafo1(e)
        )

        self._txt_info_grafo1 = ft.Text("", size=14)

        self._lista_grafo1 = ft.ListView(
            controls=[],
            height=300,
            spacing=5,
            auto_scroll=False
        )

        self.controls.clear()
        self.controls.extend([
            ft.Container(height=10),
            self._title,
            self._subtitle,
            insights_section
        ])

        # Aggiungo la View alla pagina se non è già presente
        if self not in self._page.controls:
            self._page.add(self)

        self._page.update()

        # Caricamento automatico degli insight dal controller
        if self._controller is not None:
            self._controller.load_insights()

    def _crea_card_lista(self, titolo, width=330):
        lista = ft.Column(controls=[], spacing=6)

        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        titolo,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#1f3b4d"
                    ),
                    ft.Divider(height=10, color="#d0d7de"),
                    lista
                ],
                spacing=6
            ),
            padding=18,
            width=width,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color="#00000022",
                offset=ft.Offset(0, 2)
            )
        )


        return card, lista

    def _crea_card_numero(self, titolo, icona):
        txt_valore = ft.Text(
            "-",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="#1f3b4d"
        )

        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(icona, size=26),
                    ft.Text(titolo, size=15, color="#52616b"),
                    txt_valore
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=18,
            width=220,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color="#00000022",
                offset=ft.Offset(0, 2)
            )
        )

        return card, txt_valore

    def aggiorna_lista(self, lista_control, items):
        """Aggiorna una card contenente una classifica."""
        lista_control.controls.clear()

        if not items:
            lista_control.controls.append(
                ft.Text("Nessun dato disponibile", size=13, italic=True, color="#7a7a7a")
            )
        else:
            for i, item in enumerate(items, start=1):
                lista_control.controls.append(
                    ft.Text(f"{i}. {item}", size=13, color="#263238")
                )

        self.update()

    def aggiorna_numero(self, text_control, valore):
        """Aggiorna una card numerica."""
        text_control.value = str(valore)
        self.update()

    def aggiorna_insights(
            self,
            top_brani=None,
            top_artisti=None,
            top_generi=None,
            num_clienti=0,
            num_fatture=0,
            num_tracce=0,
            top_clienti_spesa=None,
            top_artisti_clienti=None
    ):
        """Metodo pubblico chiamato dal controller per popolare la dashboard."""

        self.aggiorna_lista(self._lista_top_brani, top_brani or [])
        self.aggiorna_lista(self._lista_top_artisti, top_artisti or [])
        self.aggiorna_lista(self._lista_top_generi, top_generi or [])

        self.aggiorna_numero(self._txt_num_clienti, num_clienti)
        self.aggiorna_numero(self._txt_num_fatture, num_fatture)
        self.aggiorna_numero(self._txt_num_tracce, num_tracce)

        self.aggiorna_lista(self._lista_top_clienti_spesa, top_clienti_spesa or [])
        self.aggiorna_lista(self._lista_top_artisti_clienti, top_artisti_clienti or [])

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller
