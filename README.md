# chess_server_strong
Dieses Repository stellt im Rahmen der Projektarbeit im Fach **Sichere Programmierung** das Projekt **chess_server** in der starken Version zur Verfügung.

## Getting started
### Prerequisites
Die benötigten Packages von der _requirements.txt_ Datei installieren:

- ```pip install -r requirements.txt```


## Usage
### Allgemein
Um das Projekt zu benutzen, muss man den Server starten und sich dann mit einem Client verbinden.
### Server
Um den Server zu starten, muss lediglich die Datei _main.py_ ausgeführt werden:
- ```python3 ./main.py```

Dadurch startet der Server automatisch mit der verwendeten IP-Adresse auf dem Port **8080**


### Client
Um den Client zu starten und somit eine Verbindung zum Server zu erhalten, muss lediglich die Datei _client.py_ ausgeführt werden:
- ```python3 ./client.py```

Dadurch verbindet sich der Client mit dem Server anhand der automatisch verwendeten IP-Adresse auf dem Port **8080**


## Struktur
### Anhang
In dem Ordner _Anhang_ befindet sich sowohl die Dokumentation in Form der PDF-Datei _Doc-ChessProg.pdf_, als auch weitere relevante Inhalte:
- brute_force.py: Quellcode des Brute-Force-Angriffes
- Brute_Force_Plaintext.xlsx: Excel-Datei für die Berechnung des CWSS-Scores des Passwortes und des Aktivierungscodes
- Calculation_Password-Options.pdf: Berechnungen der Komplexität und Aufwand eines Brute-Force Angriffes eines Passwortes der umgesetzten Passwortrichtlinie
- Doc-ChessProg.pdf: Dokumentation des Projektes
- dos.py: Quellcode des DOS-Angriffes
- Erläuterung der CWSS-Bepunktung.pdf: Erläutert die einzelnen Kriterien der CWSS-Bepunktung
- get_menu_choice.py: Quellcode aus der Datei _controller.py_; zeigt die in der Dokumentation erwähnte Rekursion
- man-in-the-middle.xlsx: Excel-Datei für die Berechnung des CWSS-Scores der Kommunikation
- sql_injection.xlsx: Excel-Datei für die Berechnung des CWSS-Scores der Datenbank
- statistik_1.xlsx: Zeigt Auswirkungen der DOS-Attacke auf den Server in Einer-Schritten
- statistik_2.xlsx: Zeigt Auswirkungen der DOS-Attacke auf den Server in Zwanziger-Schritten
