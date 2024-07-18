# ---- Ten plik zawiera template bazowego pliku. ---

class XlsxWzor: 
    # Ten plik zawiera nazwy kolumn, które są w głównym pliku.

    NAZWA_ARKUSZA: str = "DANE WEJŚCIOWE"

    NUMER_ELEMENTU = ""
    NUMER_WNIOSKU: str = "NUMER_WNIOSKU"
    KANAŁ: str = "KANAŁ"
    STATUS: str = "STATUS"
    DATA_UTWORZENIA: str = "DATA_UTWORZENIA"
    DATA_ZATWIERDZENIA: str = "DATA_ZATWIERDZENIA"
    DATA_URUCHOMIENIA: str = "DATA_URUCHOMIENIA"
    KOD_PRODUKTU: str = "KOD_PRODUKTU"
    GOTÓWKA: str = "GOTÓWKA"
    SUMA_KONSOLIDACJI: str = "SUMA_KONSOLIDACJI"
    OPŁATA_BR: str = "OPŁATA_BR"
    BRUTTO: str = "BRUTTO"
    ILOSC_RAT: str = "ILOSC_RAT"
    OPROCENTOWANIE: str = "OPROCENTOWANIE"
    PROWIZJA: str = "PROWIZJA_PROCENT"
    KOD_OFERTY: str = "KOD_OFERTY"
    RODZAJ_OPROCENTOWANIA: str = "RODZAJ_OPROCENTOWANIA"
    OCENA_RYZYKA: str = "OCENA_SYZYKA"

    # Helper
    ZAKRES_DATY = "ZAKRES_DATY"

    # Używane do summaryzatora
    PLIK_ŹRÓDŁOWY_NAZWA = "Plik źródłowy nazwa"
    PLIK_ŹRÓDŁOWY_ŚCIEŻKA = "Plik źródłowy ścieżka"

    @classmethod
    def wez_wszystkie_kolumny(cls) -> list[str]:
        """Bierze wszystkie kolumny, jakie powinny być w pliku."""

        return [
            cls.NUMER_ELEMENTU,
            cls.NUMER_WNIOSKU,
            cls.KANAŁ,
            cls.STATUS,
            cls.DATA_UTWORZENIA,
            cls.DATA_ZATWIERDZENIA,
            cls.DATA_URUCHOMIENIA,
            cls.KOD_PRODUKTU,
            cls.GOTÓWKA,
            cls.SUMA_KONSOLIDACJI,
            cls.OPŁATA_BR,
            cls.BRUTTO,
            cls.ILOSC_RAT,
            cls.OPROCENTOWANIE,
            cls.PROWIZJA,
            cls.KOD_OFERTY,
            cls.RODZAJ_OPROCENTOWANIA,
            cls.OCENA_RYZYKA
        ]
    
    @classmethod
    def wez_najważniejsze_kolumny(cls) -> list[str]:
        """Wykaz kolumn, które pokażą się jako print element. """

        return [
            cls.NUMER_WNIOSKU,
            cls.KANAŁ,
            cls.DATA_URUCHOMIENIA,
            cls.ZAKRES_DATY,
            cls.GOTÓWKA,
            cls.PROWIZJA,
            cls.ILOSC_RAT,
            cls.RODZAJ_OPROCENTOWANIA,
            cls.KOD_PRODUKTU,
            cls.OCENA_RYZYKA
        ]