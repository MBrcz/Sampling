Aplikacja CML (Command Line App) do oznaczania próbek według arbitralnie zdefiniowanych kryteriów.
Dokładna deklaracja procedury wybierania próbek znajduje się w module samples.py

SETUP:
1) Pobierz Repo,
2) Wypakuj gdzieś pliki,
3) Postaw nowy venv według komend:
   cd {ścieżka} && {lewy(ścieżka, 1)} && rmdir /s /q venv && python -m venv venv && venv\scripts\activate && pip install -r requirements.txt
4) Teraz powinno dać się odpalić aplikację.

Jak używać?
Aplikacja jest CML (Command Line Application), jej punktem wejścia jest plik main.py która posiada 2 komendy:
a) zaznacz [arg:=ścieżka] - zaznacza próbki w wszyskich plikach, które są w odległości 2 folderów od Głównego Folderu
b) ukryj   [arg:=ścieżka] - usuwa zaznaczone próbki.


Najważniejsze moduły / informacje:
a) functions.py - zawiera zbiór deklaracji funkcji używanych w projekcie.
b) samples.py   - zawiera logikę oraz procedurę wybierania próbek.
c) utils.py     - funkcje stricte pomocnicze, nie ma tam nic ciekawego.
d) xlsx_blacklist.py - czarna lista plików Excel, które będą pomijane przez skrypt.
e) xlsx_handler.py - zawiera logikę i zbiór postępowania przy operacjach stricte Excelowskich.
f) xlsx_template.py - zawiera wykaz nazw kolumn w plikach do próbkowania, z których będą wybierane próbki.
-------------------------------------------------------