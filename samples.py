# Ten moduł odpowiedzialny jest stricte za losowanie próbek do projektu.
import pandas as pd
from xlsx_template import XlsxWzor
from random import shuffle

# Jak działa ten skrypt:
# UWAGA! Każdy element wybierany jest tabeli, dla której w chwili obecnej jest NAJMNIEJSZA ilość zakresów dat!

# Niech frame = tabela (dla uproszczenia, pomimo że to teoretycznie nie to samo).
# a) Wybiera wszystkie kanały z tabelki,
# b) Dla kanału:
#    I. Przefiltrowywuje przez wybrane zakresy dat (0, 1, 2)
#    Ia. Usuwa wszystkie, elementy dla których data wyboru jest mniejsza i większa od 3 od wybranych już elementów.
#    II. Sprawdza czy gotówka jest więskza od 75k i nie ma wybranego nic z gotówką większą niż 75k
#       1. Jeśli tak: wybiera element z najmniejszą ilością zakresów dat, z tabelka, gdy gotówka >= 75k
#       2. Jeśli nie: pomija
#    III. Sprawdza czy został wybrany element z oceną ryzyka [S09, S10, S11] lub [S01, S02 ... S07] (kolejność losowa) 
#       1. Jeśli tak - pomija
#       2. Jeśli nie - zawęża zmiany i wybiera element z najmniejszą ilością zakresów dat.
#    IV. Odfiltrowywuje losowo wybrane już filtry z kolumn (zobacz deklarację: self.filtry). 
#        Wybiera tą tabelkę dla której tabela <> 0 i ilość odfiltrowanych elementów jest największa.

class Probkowanie:
    def __init__(self, content: pd.DataFrame) -> None:
        self.próbki: dict = {} # Wybrane próbki z zakresów.
        self.filtry: dict = {} # Zobacz więcej w _dodaj_filtry_do_trackowania 
        self.zawartosc: pd.DataFrame = content    

    def wylosuj_próbki(self):
        """Zajmuje się losowaniem próbek - główna i jedyna methoda do wywoływania z zewnątrz."""

        # Dzieli tabelę na zakresy grup.
        self.zawartosc[XlsxWzor.ZAKRES_DATY] = self.zawartosc[XlsxWzor.DATA_URUCHOMIENIA].apply(lambda data: int(data.day / (10 + 1)))
        zawartosc_grupy: tuple = self.zawartosc.groupby(XlsxWzor.KANAŁ)

        for kanał, grupa in zawartosc_grupy:
            # To są filtry traktowane priorytetowo.
            self.filtry[kanał] = {
                XlsxWzor.ZAKRES_DATY: [],    # To jest wyjątek.
                XlsxWzor.DATA_URUCHOMIENIA: [], # To jest wyjątek 2
                XlsxWzor.PROWIZJA: [],
                XlsxWzor.OPROCENTOWANIE: [],
                XlsxWzor.ILOSC_RAT: [],
                XlsxWzor.RODZAJ_OPROCENTOWANIA: [],
                XlsxWzor.KOD_PRODUKTU: [],
                XlsxWzor.OCENA_RYZYKA: []
            }
            self.próbki[kanał] = []

            # -------- Pętla, która losuje elementy. -------------
            for _ in range(3):
                data_frame: pd.DataFrame = self._zawęź_zawartość_do_wyboru(grupa, kanał)
                if len(data_frame) == 0:
                    print(f"Uwaga! Kanał {kanał[0]} ma mniej niż 3 elementy do wyboru!")
                    return
                
                nazwa_wniosku: str = self._wylosuj_wniosek_z_najmniejszym_zakresem_dat(data_frame)
                self.próbki[kanał].append(nazwa_wniosku)
                self._dodaj_filtry_do_trackowania(kanał=kanał, wniosek=nazwa_wniosku)

    def _dodaj_filtry_do_trackowania(self, kanał: int, wniosek: str) -> None:
        """Dodaje filtry, które zostały już użyte do sprawdzania. """

        for kolumna in self.filtry[kanał]:
            wybrany_wiersz = self.zawartosc[self.zawartosc[XlsxWzor.NUMER_WNIOSKU] == wniosek]
            self.filtry[kanał][kolumna].append(wybrany_wiersz.iloc[0][kolumna])

    def _zawęź_zawartość_do_wyboru(self, grupa: pd.DataFrame, kanał: int) -> pd.DataFrame:
        """ Zawęża maksymalnie w dół frame odpowiedzialny za wybór zawartości."""

        frame: pd.DataFrame = grupa.copy()
        # Wywala wszyskie elementy już nałożone przez zakres daty.
        for zakres in self.filtry[kanał][XlsxWzor.ZAKRES_DATY]:
            frame = frame[frame[XlsxWzor.ZAKRES_DATY] != zakres]

            # Jeśli ilość elementów jest rowna 0, wróć do grupy.
            if len(frame) == 0:
                frame = grupa.copy()
                break
            
        # Usuwa wszystkie elementy, gdzie daty są 3 dni przed i 3 dni po już wybranym elementcie.
        tymcz_frame: pd.DataFrame = frame.copy()
        for data in self.filtry[kanał][XlsxWzor.DATA_URUCHOMIENIA]:
            frame = frame.loc[~frame[XlsxWzor.DATA_URUCHOMIENIA].between(data - pd.Timedelta(days=3), data + pd.Timedelta(days=3))]

            if len(frame) == 0:
                frame = tymcz_frame.copy()
                break

        # Wiersze wybrane już przez skrypt.
        wybrane_frame: pd.DataFrame = self._weź_wybrane_próbki_jako_frame(kanał)
        
        # Radzi sobie z gotówką.
        wartość_gotówki: int = 75000
        if len(wybrane_frame.loc[wybrane_frame[XlsxWzor.GOTÓWKA] >= wartość_gotówki]) == 0 and len(frame.loc[frame[XlsxWzor.GOTÓWKA] >= wartość_gotówki]) > 1:
            frame = frame.loc[frame[XlsxWzor.GOTÓWKA] >= wartość_gotówki]

       # Wybierz S09, S10 lub S11 jeśli to możliwe
        ryzyka: list[list[str]] = [["S09", "S10", "S11"], ["S01", "S02", "S03", "S04", "S05", "S06", "S07"]]
        shuffle(ryzyka)   # Zamienia pozycję listy w ryzykach na 0, 1 i 1, 0 - dodaje trochę nieprzewidywalności skryptowi. Usuń jeśli irytuje.
        for ryzyko in ryzyka:
            if len(wybrane_frame.loc[wybrane_frame[XlsxWzor.OCENA_RYZYKA].isin(ryzyko)]) == 0 and len(frame.loc[frame[XlsxWzor.OCENA_RYZYKA].isin(ryzyko)]) >= 1:
                frame = frame.loc[frame[XlsxWzor.OCENA_RYZYKA].isin(ryzyko)]
                break

        # Przefiltrowywuje w opór ile się da
        nałożone_filtry: dict = {}
        pozostały_frame: pd.DataFrame = frame.copy()
    
        for kolumna, wartości in self.filtry[kanał].items():
            # Jeśli kolumną, jest zakres daty, pomiń
            if kolumna == XlsxWzor.ZAKRES_DATY or kolumna == XlsxWzor.DATA_URUCHOMIENIA:
                continue

            tymcz_df: pd.DataFrame = pozostały_frame[~pozostały_frame[kolumna].isin(wartości)]

            if not tymcz_df.empty:
                nałożone_filtry[kolumna] = wartości
                pozostały_frame = tymcz_df
        
        return pozostały_frame

    def _weź_wybrane_próbki_jako_frame(self, kanał: str) -> pd.DataFrame:
        """Bierze wybrane próbki jako data frame."""

        return self.zawartosc.loc[self.zawartosc[XlsxWzor.NUMER_WNIOSKU].isin(self.próbki[kanał])]
    
    def _wylosuj_wniosek_z_najmniejszym_zakresem_dat(self, df: pd.DataFrame) -> str:
        """Losuje element, który ma najmniejszą ilość temp w framie. """
        
        najmniejsza_wartość_zakresu: str = min(df[XlsxWzor.ZAKRES_DATY])
        df = df[df[XlsxWzor.ZAKRES_DATY] == najmniejsza_wartość_zakresu]
        return df.sample(n=1).iloc[0][XlsxWzor.NUMER_WNIOSKU]
