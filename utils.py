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
            funckja(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())

            ans = ""
            while ans != "":
                ans = input("Naciśnij cokolwiek aby wyjść z procedury!")
    
    return _exec

def znajdź_wszystkie_pliki_excela(ścieżka: str, głębokość: int = 2):
    """Znajduje wszystkie pliki należące do Excela zaczynając od podanej ścieżki."""

    print(f"Szukanie plików Excela w {ścieżka} dla głębokości: {głębokość}")    
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
    print(f'Znaleziono łącznie: {len(znalezione_pliki)} plików!')
    return znalezione_pliki


def usuń_plik(ścieżka: str) -> None:
    """Jak nazwa wskazuje, stara się usunąć plik."""

    try:
        remove(ścieżka)
        print(f"Usunięto z powodzeniem plik: {ścieżka}")
    except Exception as e:
        print(f"Nie można usunąć pliku: {ścieżka} ze względu na {e}")
