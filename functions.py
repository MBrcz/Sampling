import utils as ut
from xlsx_handler import XlsxHandler, pd
from os.path import join, basename

@ut.prosty_error_wrapper
def zaznacz_próbki(ścieżka_folderu_głównego: str) -> None:
    """Odpowiada za zaznaczanie próbek."""

    print("Rozpoczęcie procedury: ")
    plik_pods_ścieżka: str = join(ścieżka_folderu_głównego, ut.XlsxCzarnaLista.PODSUMOWANIE)
    print(plik_pods_ścieżka)
    pliki: list[str] = ut.znajdź_wszystkie_pliki_excela(ścieżka_folderu_głównego)
    
    xlsxhandler = XlsxHandler()
    lista_frame: list[pd.DataFrame] = []
    for plik in pliki:  
        xlsxhandler.otwórz_plik(plik)
        xlsxhandler.wylosuj_próbki()
        xlsxhandler.pokoloruj_plik()
        lista_frame.append(xlsxhandler.zapisz_wybrane_próbki())
        print(f"Zakończono zaznaczanie dla pliku: {basename(plik)}")
        print(f"Wybrano łącznie: {len(xlsxhandler.probki)} elementów!")
    
    wszystkie_frame: pd.DataFrame = pd.concat(lista_frame, axis=0, ignore_index=True)
    wszystkie_frame.to_excel(plik_pods_ścieżka)
    print(f"Stworzono plik podsumowujący operację w: {plik_pods_ścieżka}")
    print("Działanie programu zakończone sukcesem!")


@ut.prosty_error_wrapper
def zresetuj_próbki(ścieżka_folderu_głównego: str) -> None:
    """Odpowiada za zaznaczanie próbek."""

    print("Rozpoczęcie procedury: ")
    print("Próbuje usunąć arkusz podsumowujący: ")
    pliki: list[str] = ut.znajdź_wszystkie_pliki_excela(ścieżka_folderu_głównego)

    xlsxhandler = XlsxHandler()
    for plik in pliki:  
        xlsxhandler.otwórz_plik(plik)
        xlsxhandler.pokoloruj_plik()
        print(f"Usuwanie dla pliku: {basename(plik)}" )
    ut.usuń_plik(join(ścieżka_folderu_głównego, ut.XlsxCzarnaLista.PODSUMOWANIE))
    print("Działanie programu zakończone sukcesem!")
