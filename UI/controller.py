class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def load_insights(self):
        """Carica gli insight iniziali dal model e aggiorna le card della dashboard."""

        # Riga 1: classifiche principali
        top_brani = self._format_items(self._model.get_top_five_tracks())
        top_artisti = self._format_items(self._model.get_top_five_artists())
        top_generi = self._format_items(self._model.get_top_five_genres())

        self._view.aggiorna_lista(self._view._lista_top_brani, top_brani)
        self._view.aggiorna_lista(self._view._lista_top_artisti, top_artisti)
        self._view.aggiorna_lista(self._view._lista_top_generi, top_generi)

        # Riga 2: numeri generali
        self._view.aggiorna_numero(self._view._txt_num_clienti, self._model.get_num_customers())
        self._view.aggiorna_numero(self._view._txt_num_fatture, self._model.get_num_fatture())
        self._view.aggiorna_numero(self._view._txt_num_tracce, self._model.get_num_tracks())

        # Riga 3: insight avanzati
        top_clienti_spesa = self._format_items(self._model.get_top_3_spenders())
        top_artisti_clienti = self._format_items(self._model.get_top_3_artist_with_more_different_clients())

        self._view.aggiorna_lista(self._view._lista_top_clienti_spesa, top_clienti_spesa)
        self._view.aggiorna_lista(self._view._lista_top_artisti_clienti, top_artisti_clienti)

    def _format_items(self, items):
        """
        Converte in stringhe i risultati restituiti dal model.

        Gestisce:
        - oggetti dataclass, es. Track, Artist, Genre
        - tuple, es. ('Mario', 'Rossi', 45.90)
        - dizionari
        - stringhe/numeri semplici
        """
        formatted = []

        if items is None:
            return formatted

        for item in items:
            formatted.append(self._format_single_item(item))

        return formatted

    def _format_single_item(self, item):
        """Formatta un singolo elemento in modo leggibile per la GUI."""

        # Caso dizionario
        if isinstance(item, dict):
            return " - ".join(str(v) for v in item.values())

        # Caso tuple/list, es. ('Mario', 'Rossi', 45.9)
        if isinstance(item, (tuple, list)):
            return " - ".join(str(v) for v in item)

        # Caso oggetto con attributo Name, tipico di Track, Artist, Genre
        if hasattr(item, "Name"):
            return str(item.Name)

        # Alcune dataclass potrebbero avere name minuscolo
        if hasattr(item, "name"):
            return str(item.name)

        # Cliente con nome e cognome
        if hasattr(item, "FirstName") and hasattr(item, "LastName"):
            return f"{item.FirstName} {item.LastName}"

        # Fallback: usa lo __str__ dell'oggetto
        return str(item)

