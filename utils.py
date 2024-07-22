# Ten moduł zawiera funkcje stricte użytecznościowe.
import traceback
from os.path import isdir, join
from os import listdir, remove
from xlsx_blacklist import XlsxCzarnaLista

def prosty_error_wrapper(funckja: callable, *args, **kwargs) -> callable:
    """Wykonuje procedurę i odpowiada za łatwy error handling"""

    def _exec(*args, **kwargs):
        """Funkcja wewnętrzna, która działa jako exit point apki"""
        try:
            return funckja(*args, **kwargs)
        except PermissionError as e:
            print(traceback.format_exc())
            print("*** Permission error polega na tym, że proces który skrypt próbuje otworzyć jest już używany przez Twój komputer.\n"
                  "Wylącz Excele, które skrypt próbuje otworzyć i powinno działać. ***")
        except Exception as e:
            print(traceback.format_exc())
    
    return _exec

def znajdź_wszystkie_pliki_excela(ścieżka: str, głębokość: int = 2, drukuj: bool = True):
    """Znajduje wszystkie pliki należące do Excela zaczynając od podanej ścieżki."""

    if drukuj: print(f"Szukanie plików Excela w {ścieżka} dla głębokości: {głębokość}")    
    dopuszczalne_rozszerzenia = [".xlsm", ".xlsx", ".xls"]
    znalezione_pliki = []

    def przejdź_dalej(obecna_ścieżka: str, current_depth):

        if current_depth > głębokość:
            return
        
        try:
            for objekt in listdir(obecna_ścieżka):
                pełna_ścieżka = join(obecna_ścieżka, objekt)
                if isdir(pełna_ścieżka):
                    przejdź_dalej(pełna_ścieżka, current_depth + 1)
                else:
                    # Jeśli plik znajduje się w czarnej liście, pomiń
                    if pełna_ścieżka.split("\\")[-1] in XlsxCzarnaLista.weź_wszystkie_pliki_z_czarnej_list():
                        continue

                    elif any(pełna_ścieżka.endswith(ext) for ext in dopuszczalne_rozszerzenia):
                        znalezione_pliki.append(pełna_ścieżka)
        except PermissionError:
            print(f'Błąd dostępu: {pełna_ścieżka}')

    przejdź_dalej(ścieżka, 0)
    if drukuj: print(f'Znaleziono łącznie: {len(znalezione_pliki)} plików!')
    return znalezione_pliki


def usuń_plik(ścieżka: str) -> None:
    """Jak nazwa wskazuje, stara się usunąć plik."""

    try:
        remove(ścieżka)
        print(f"Usunięto z powodzeniem plik: {ścieżka}")
    except Exception as e:
        print(f"Nie można usunąć pliku: {ścieżka} ze względu na {e}")


def znajdź_wspólne_elementy_w_wartościach_słownika(słownik: dict[str: list[str]]) -> list[str]:
    """Znajduje współne elementy w wartościach słownika. """

    sets: list[set] = [set(lst) for lst in słownik.values()]

    if sets:
        common_elements: set = set.intersection(*sets)
    else:
        common_elements: set = set()

    wynik: list[set] = list(common_elements)
    wynik.sort()
    return wynik
