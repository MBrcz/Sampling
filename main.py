import functions as func
import argparse
from utils import prosty_error_wrapper

# Główny punkt wejścia do aplikacji.

# Najważniejsze moduły / informacje:
# a) functions.py - zawiera zbiór deklaracji funkcji używanych w projekcie.
# b) samples.py   - zawiera logikę oraz procedurę wybierania próbek.
# c) utils.py     - funkcje stricte pomocnicze, nie ma tam nic ciekawego.
# d) xlsx_blacklist.py - czarna lista plików Excel, które będą pomijane przez skrypt.
# e) xlsx_handler.py - zawiera logikę i zbiór postępowania przy operacjach stricte Excelowskich.
# f) xlsx_template.py - zawiera wykaz nazw kolumn w plikach do próbkowania, z których będą wybierane próbki.

# -------------------------------------------------------
# Jak używać?
# Aplikacja jest CML (Command Line Application), która posiada 2 komendy:
# a) zaznacz [arg:=ścieżka] - zaznacza próbki w wszyskich plikach, które są w odległości 2 folderów od Głównego Folderu
# b) ukryj   [arg:=ścieżka] - usuwa zaznaczone próbki.

# Tak więc:
# a) Otwórz CMD,
# b) cd {ścieżka do aplikacji} && {pierwsza literka ścieżki}:
# c) venv\Scripts\activate && main.py {komenda} {arg}
# Lista niezbędnych bibliotek znajduje się w requirements.txt.

# Opis działania aplikacji znajduje się w pliku: samples.py

@prosty_error_wrapper
def main():
    """Punkt wejścia do aplikacji. """
    parser = argparse.ArgumentParser(description="Process some files.")
    
    subparsers = parser.add_subparsers(dest="command", help="Wpisz '-h'")    
    parser_zaznacz = subparsers.add_parser("zaznacz", help="Zaznacza zawartość w plikach (próbkuje).")
    parser_zaznacz.add_argument("ścieżka", type=str, help="Ścieżka do podstawowego folderu.")
    parser_zaznacz.add_argument('daty', nargs="?", help=("Daty, w ramach których skrypt będzie działał. "
                                                         "Dodawać jako tekst, można dać jedną datę lub dwie. Format daty to jest dd.mm.YYYY - np:\n"
                                                         "1.\"22.02.2024\" - taki zapis wybierze tylko jedną datę\n"
                                                         "2.\"22.02.2024,24.02.2024\" - wybierze daty pomiędzy tymi dwoma datami."))

    parser_usun = subparsers.add_parser("ukryj", help="Usuwa zaznaczoną zawartość w plikach (anty-próbkuje)")
    parser_usun.add_argument("ścieżka", type=str, help="Ścieżka do podstawowego folderu.")

    parser_daty = subparsers.add_parser("daty", help="Wypisuje daty, jakie można użyć jako argumenty.")
    parser_daty.add_argument("ścieżka", help="Ścieżka do podstawowego folderu.")

    args = parser.parse_args()

    if args.command == "zaznacz":
        if args.daty:
            if "," in args.daty:
                daty = args.daty.split(",")[:2]
            else:
                daty = [args.daty, args.daty]
        else:
             daty = []

        func.zaznacz_próbki(args.ścieżka.replace("\"", ""), daty)
    elif args.command == "ukryj":
        func.zresetuj_próbki(args.ścieżka.replace("\"", ""))
    elif args.command == "daty":
        func.sprawdź_ważne_daty(args.ścieżka.replace("\"", ""))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
