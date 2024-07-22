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

Jak działa próbkowanie (dobór próbek):
# Jak działa ten skrypt:
# UWAGA! Każdy element wybierany jest tabeli, dla której w chwili obecnej jest NAJMNIEJSZA ilość zakresów dat!

# Niech frame = tabela (dla uproszczenia, pomimo że to teoretycznie nie to samo).
a) Wybiera wszystkie kanały z tabelki,
b) Dla kanału:
   I. Przefiltrowywuje przez wybrane zakresy dat (0, 1, 2)
   Ia. Usuwa wszystkie, elementy dla których data wyboru jest mniejsza i większa o 3 od wybranych już elementów.
       Np. Jeśli został wybrany 05.02.2024 to wywala daty od 02.02.2024 do 08.02.2024. W przypadku, gdy nie ma wolnych dat, ignoruje ten krok.
   II. Sprawdza czy gotówka jest więskza od 75k i nie ma wybranego nic z gotówką większą niż 75k
      1. Jeśli tak: wybiera element z najmniejszą ilością zakresów dat, z tabelka, gdy gotówka >= 75k
      2. Jeśli nie: pomija
   III. Sprawdza czy został wybrany element z oceną ryzyka [S09, S10, S11] lub [S01, S02 ... S07] (kolejność losowa) 
      1. Jeśli tak - pomija
      2. Jeśli nie - zawęża zmiany i wybiera element z najmniejszą ilością zakresów dat.
   IV. Odfiltrowywuje losowo wybrane już filtry z kolumn (zobacz deklarację: self.filtry). 
       Wybiera tą tabelkę dla której tabela <> 0 i ilość odfiltrowanych elementów jest największa.
Jeśli nie ma 3 unikatowych kanałów to bierze z 2, jak nie ma 2 to z 1.
