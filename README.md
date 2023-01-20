# chess_server_strong
Dieses Repository stellt im Rahmen der Projektarbeit im Fach **Sichere Programmierung** das Projekt **chess_server** in der starken Version zur Verfügung.

## Getting started
### Prerequisites
Die benötigten Packages von der _requirements.txt_ Datei installieren:

- ```pip install -r requirements.txt```


## Usage
### Allgemein
Um das Projekt zu benutzen, muss man den Server starten und sich als Client mit dem Server verbinden.
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
- Auflistung der CWEs.docx: Eine Liste von allen gefundenen CEWs des Programmes in der schwachen und starken Version als Word-Datei
- Auflistung der CWEs.pdf: Eine Liste von allen gefundenen CEWs des Programmes in der schwachen und starken Version als PDF-Datei
- Auswirkung DOS Attacke Sprungweite 1.xlsx: Zeigt Auswirkungen der DOS-Attacke auf den Server in Einer-Schritten
- Auswirkung DOS Attacke Sprungweite 20.xlsx: Zeigt Auswirkungen der DOS-Attacke auf den Server in Zwanziger-Schritten
- Berechnung CWSS-Score (Datenbank).xlsx: Excel-Datei für die Berechnung des CWSS-Scores der Datenbank
- Berechnung CWSS-Score (Kommunikation).xlsx: Excel-Datei für die Berechnung des CWSS-Scores der Kommunikation
- Berechnung CWSS-Score (Passwort).xlsx: Excel-Datei für die Berechnung des CWSS-Scores des Passwortes und des Aktivierungscodes
- Calculation_Password-Options.pdf: Berechnungen der Komplexität und Aufwand eines Brute-Force Angriffes eines Passwortes der umgesetzten Passwortrichtlinie
- Doc-ChessProg.pdf: Dokumentation des Projektes
- Erläuterung der CWSS-Bepunktung.pdf: Erläutert die einzelnen Kriterien der CWSS-Bepunktung
- Präsentation.pptx: PowerPoint-Datei für die Präsentation
- Quellcode Ausschnitt get_menu_choice.py: Quellcode aus der Datei _controller.py_; zeigt die in der Dokumentation erwähnte Rekursion
- Quellcode brute-force-Attacke.py: Quellcode des Brute-Force-Angriffes
- Quellcode DOS-Attacke.py: Quellcode des DOS-Angriffes
