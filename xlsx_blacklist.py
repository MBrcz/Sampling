# Ten plik gromadzi nazwy plików xlsx, które będą pomijane przez skrypt


class XlsxCzarnaLista:
    PODSUMOWANIE: str = "Podsumowanie.xlsx"
    # Dodaj więcej!


    @classmethod
    def weź_wszystkie_pliki_z_czarnej_list(cls):
        """Zgarnia nazwy wszystkich plików, które będą ignorowane"""

        return [getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith('__')]
    