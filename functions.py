# Ten moduł przechowuje wszystkie funkcje używane poprzez CMD.
import utils as ut
from xlsx_handler import XlsxHandler, pd
from os.path import join, basename
from datetime import datetime

@ut.prosty_error_wrapper
def zaznacz_próbki(ścieżka_folderu_głównego: str, daty: list[str]=[]) -> None:
    """Odpowiada za zaznaczanie próbek."""

    print("Rozpoczęcie procedury: ")
    plik_pods_ścieżka: str = join(ścieżka_folderu_głównego, ut.XlsxCzarnaLista.PODSUMOWANIE)
    pliki: list[str] = ut.znajdź_wszystkie_pliki_excela(ścieżka_folderu_głównego)

    # DATY.
    if daty:
        if not all(d in sprawdź_ważne_daty(ścieżka_folderu_głównego, False) for d in daty):
            raise ValueError("Podano zły zakres daty! Wpisz -daty, aby dowiedzieć się więcej!")
        elif datetime.strptime(daty[0], "%d.%m.%Y") > datetime.strptime(daty[1], "%d.%m.%Y"):
            raise TypeError("Dolna data jest wyższa od górnej! To nie ma sensu!")
        
        print(f"Zaakceptowano zakres dat, w ramach których wybierane będą próbki: {daty}")
    
    excel: XlsxHandler = XlsxHandler()
    lista_frame: list[pd.DataFrame] = []
    for plik in pliki:  
        excel.otwórz_plik(plik)
        excel.zmodyfikuj_zawartość_o_daty(daty)
        excel.wylosuj_próbki()
        excel.pokoloruj_plik()
        lista_frame.append(excel.zapisz_wybrane_próbki())
        print(f"Zakończono zaznaczanie dla pliku: {basename(plik)}")
        print(f"Wybrano łącznie: {len(excel.probki)} elementów!")
    
    wszystkie_frame: pd.DataFrame = pd.concat(lista_frame, axis=0, ignore_index=True)
    wszystkie_frame.to_excel(plik_pods_ścieżka)
    print(f"Stworzono plik podsumowujący operację w: {plik_pods_ścieżka}")
    print("Działanie programu zakończone sukcesem!")


@ut.prosty_error_wrapper
def zresetuj_próbki(ścieżka_folderu_głównego: str) -> None:
    """Odpowiada za zaznaczanie próbek."""

    print("Rozpoczęcie procedury: ")
    pliki: list[str] = ut.znajdź_wszystkie_pliki_excela(ścieżka_folderu_głównego, False)

    excel: XlsxHandler = XlsxHandler()
    for plik in pliki:  
        excel.otwórz_plik(plik)
        excel.pokoloruj_plik()
        print(f"Usuwanie dla pliku: {basename(plik)}" )
    print("Próbuje usunąć arkusz podsumowujący: ")
    ut.usuń_plik(join(ścieżka_folderu_głównego, ut.XlsxCzarnaLista.PODSUMOWANIE))
    print("Działanie programu zakończone sukcesem!")


@ut.prosty_error_wrapper
def sprawdź_ważne_daty(ścieżka_folderu_głównego: str, konsola: bool=True) -> list[str]:
    """Sprawdza, jakie są możliwe do wpisania daty jako argumenty."""

    if konsola: print("Rozpoczęcie procedury: ")
    pliki: list[str] = ut.znajdź_wszystkie_pliki_excela(ścieżka_folderu_głównego, drukuj=konsola)

    excel: XlsxHandler = XlsxHandler()
    
    wszystkie_daty: dict[str: list[str]] = {} 
    for plik in pliki:
        excel.otwórz_plik(plik)
        wszystkie_daty[plik] = excel.przeczytaj_możliwe_daty()
    
    lista_dat: list[str] = ut.znajdź_wspólne_elementy_w_wartościach_słownika(wszystkie_daty)
    if konsola: print(f"Daty możliwe do wybrania: {lista_dat}")
    return lista_dat
