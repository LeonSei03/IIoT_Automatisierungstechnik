# Industrielle IoT – Learning Factory Datenpipeline

## Überblick

Dieses Repository enthält die Abgabe zum Industrielle-IoT-Projekt der Gruppe **SiJuLe**.

Im Projekt wurde eine durchgängige IIoT-Datenpipeline umgesetzt. Die Pipeline verbindet Sensordaten der Learning Factory über MQTT mit einer Python-basierten Datenspeicherung, Visualisierung und anschließender Machine-Learning-Auswertung.

Der Fokus liegt darauf, Sensordaten nicht nur zu übertragen, sondern sie strukturiert weiterzuverarbeiten und für spätere Analysen nutzbar zu machen.

## Gesamtidee der Pipeline

Die Aufgaben bauen aufeinander auf und bilden gemeinsam folgenden Ablauf ab:

```text
Learning Factory / TwinCAT SPS
        ↓
Sensordaten erfassen
        ↓
MQTT-Broker
        ↓
Python MQTT-Subscriber
        ↓
Daten pro Flasche zusammenführen
        ↓
CSV + SQLite speichern
        ↓
Visualisierung / Dashboard
        ↓
Regression und Klassifikation
```

Die Daten werden also zunächst aus der Anlage bzw. Simulation veröffentlicht, anschließend in Python empfangen und in eine feste Tabellenstruktur gebracht. Diese gespeicherten Daten bilden danach die Grundlage für die Machine-Learning-Aufgaben.

## Ziel des Projekts

Ziel war es, eine typische industrielle Datenverarbeitungskette im kleinen Maßstab umzusetzen:

- Sensordaten aus einer Steuerung bzw. Simulation bereitstellen
- Daten über MQTT übertragen
- MQTT-Daten in Python empfangen
- mehrere Einzelereignisse zu vollständigen Flaschendatensätzen zusammenführen
- Daten dauerhaft speichern
- Daten visualisieren
- gespeicherte Daten für Regressions- und Klassifikationsmodelle verwenden

Dadurch entsteht eine durchgängige Verbindung von der Feldebene bis zur datengetriebenen Auswertung.

## Projektstruktur

```text
.
├── 12_1_1_TwinCAT/
│   └── TwinCAT-MQTT-Client und SPS-Dateien
│
├── 12_1_2_Datenspeicherung/
│   └── Python MQTT-Subscriber, Speicherung und Visualisierung
│
├── 12_3_Regression/
│   └── Lineares Regressionsmodell zur Vorhersage des Endgewichts
│
├── 12_4_Klassifikation/
│   └── Klassifikationsmodell zur Erkennung defekter Flaschen
│
└── README.md
```

Jede Teilaufgabe enthält zusätzlich eine eigene README-Datei mit genaueren Informationen zur jeweiligen Umsetzung.

## Aufgabe 12.1.1 – Daten veröffentlichen

In der ersten Teilaufgabe wurde das TwinCAT-Programm um einen MQTT-Client erweitert.

Die SPS veröffentlicht Sensordaten der Learning Factory auf dem vorgegebenen MQTT-Broker. Dabei werden statische Informationen wie Gruppenname, Namen und Einheiten einmalig gesendet. Die Messwerte werden periodisch alle 10 Sekunden aktualisiert.

Damit wird der erste Schritt der Pipeline umgesetzt:

```text
SPS / Sensorik → MQTT-Broker
```

Die Nachrichten werden retained gesendet, sodass neue MQTT-Clients direkt den letzten bekannten Wert sehen können.

Details zur TwinCAT-Umsetzung stehen in:

```text
12_1_1_TwinCAT/README.md
```

## Aufgabe 12.1.2 – Daten empfangen, transformieren und speichern

In der zweiten Teilaufgabe wurde ein Python-Skript erstellt, das MQTT-Daten vom Broker empfängt.

Die Rohdaten kommen über mehrere MQTT-Topics an. Eine einzelne Flasche erzeugt dadurch mehrere Nachrichten, zum Beispiel für Füllstände, Temperaturen, Vibrationswerte, Endgewicht und Qualitätslabel.

Diese Nachrichten werden in Python zu einem vollständigen Datensatz pro Flasche zusammengeführt.

Gespeichert wird anschließend in zwei Formen:

| Speicherform | Zweck |
|---|---|
| `data.csv` | Pflichtformat und Grundlage für die späteren ML-Aufgaben |
| `data.db` | zusätzliche SQLite-Datenbank für strukturierte Speicherung |

Zusätzlich wurden eine matplotlib-Zeitreihe und ein Streamlit-Dashboard erstellt, um die gespeicherten Daten sichtbar zu machen.

Details stehen in:

```text
12_1_2_Datenspeicherung/README.md
```

## Aufgabe 12.3 – Regression auf gespeicherten Prozessdaten

In Aufgabe 12.3 wurden die gespeicherten Daten aus der Datenspeicherung weiterverwendet.

Ziel war es, das spätere Endgewicht einer Flasche vorherzusagen. Dazu wurden Sensordaten verwendet, die bereits vor der Waage vorhanden sind.

Die Zielgröße des Modells ist:

```text
final_weight
```

Damit wird folgender Teil der Pipeline umgesetzt:

```text
gespeicherte Sensordaten → Regressionsmodell → vorhergesagtes Endgewicht
```

Das beste lineare Regressionsmodell wurde anschließend auf den bereitgestellten Datensatz `X.csv` angewendet. Die Prognosen wurden in der Datei `reg_SiJuLe.csv` gespeichert.

Details zur Feature-Auswahl, MSE/R²-Auswertung und Modellformel stehen in:

```text
12_3_Regression/README.md
```

## Aufgabe 12.4 – Klassifikation von defekten Flaschen

In Aufgabe 12.4 wurden ebenfalls die gespeicherten Daten aus der Datenspeicherung verwendet.

Ziel war es, defekte Flaschen anhand der Vibrationszeitreihe bei der Vereinzelung zu erkennen. Dafür wurden aus der Spalte `drop_oscillation` statistische Merkmale berechnet.

Die Zielklasse ist:

```text
is_cracked
```

Die verwendete Feature-Quelle ist:

```text
drop_oscillation
```

Für die Bewertung wurden verschiedene Feature-Kombinationen und Modelle verglichen. Die Ergebnisse wurden über den F1-Score bewertet und zusätzlich mit einer Confusion Matrix dargestellt.

Details zur Feature-Berechnung, F1-Tabelle und Confusion Matrix stehen in:

```text
12_4_Klassifikation/README.md
```

## Zusammenhang der Teilaufgaben

Die Teilaufgaben sind nicht unabhängig voneinander, sondern bilden gemeinsam eine vollständige Verarbeitungskette.

| Schritt | Teilaufgabe | Ergebnis |
|---|---|---|
| Sensordaten veröffentlichen | 12.1.1 | MQTT-Daten auf dem Broker |
| Daten empfangen und speichern | 12.1.2 | strukturierte CSV- und SQLite-Daten |
| Endgewicht vorhersagen | 12.3 | Regressionsmodell und `reg_SiJuLe.csv` |
| Defekte Flaschen erkennen | 12.4 | Klassifikationsmodell, F1-Tabelle und Confusion Matrix |

Die in 12.1.2 erzeugte `data.csv` ist dabei die zentrale Datengrundlage für die beiden Machine-Learning-Aufgaben.

## Wichtige Ergebnisdateien

| Datei | Bedeutung |
|---|---|
| `12_1_2_Datenspeicherung/data.csv` | gespeicherte Flaschendaten aus der MQTT-Pipeline |
| `12_1_2_Datenspeicherung/assets/zeitreihe_final_weight.png` | Plot einer ausgewählten Zeitreihe |
| `12_3_Regression/reg_SiJuLe.csv` | Prognose des Endgewichts für `X.csv` |
| `12_3_Regression/regression_feature_results.csv` | MSE- und R²-Auswertung der Regressionsmodelle |
| `12_4_Klassifikation/classification_feature_results.csv` | F1-Auswertung der Klassifikationsmodelle |
| `12_4_Klassifikation/confusion_matrix.png` | Confusion Matrix des besten Klassifikationsmodells |

## Start der Python-Skripte

Die Datenspeicherung wird im Ordner `12_1_2_Datenspeicherung` gestartet:

```bash
python main.py
```

Das Dashboard kann parallel in einem zweiten Terminal gestartet werden:

```bash
streamlit run dashboard.py
```

Der matplotlib-Plot kann zusätzlich gestartet werden:

```bash
python visualisierung.py
```

Die Machine-Learning-Aufgaben werden über die jeweiligen Jupyter Notebooks ausgeführt:

```text
12_3_Regression/regression.ipynb
12_4_Klassifikation/classification.ipynb
```