# Aufgabe 12.1.2 – Datenspeicherung und Visualisierung

## Ziel der Aufgabe

In dieser Aufgabe wurde ein Python-System entwickelt, das Sensordaten der Learning Factory über MQTT empfängt, pro Flasche zusammenführt, speichert und anschließend visualisiert.

Die Daten werden sowohl in einer CSV-Datei als auch zusätzlich in einer SQLite-Datenbank gespeichert. 

## Dateien

| Datei | Aufgabe |
|------|---------|
| `main.py` | Startet den MQTT-Subscriber und hält das Programm aktiv |
| `mqtt_client.py` | Baut die Verbindung zum MQTT-Broker auf und empfängt Nachrichten |
| `transform.py` | Führt die einzelnen Topics zu einer vollständigen Flaschen-Zeile zusammen |
| `database.py` | Speichert vollständige Flaschendaten in CSV und SQLite |
| `visualisierung.py` | Erstellt eine matplotlib-Zeitreihe und speichert den Plot |
| `dashboard.py` | Zeigt die Daten zusätzlich in einem Streamlit-Dashboard an |
| `data.csv` | CSV-Datenbank mit den gespeicherten Flaschendaten |
| `data.db` | SQLite-Datenbank mit Tabelle `flaschen` |

## MQTT-Datenquelle

- Broker: `158.180.44.197`
- Port: `1883`
- Topic: `aut/SoSe26/learning_factory_simulation/#`
- Authentifizierung: Benutzername und Passwort wurden im MQTT-Client gesetzt.

Der Subscriber empfängt alle relevanten Topics der Simulation und übergibt die Nutzdaten an die Transformationslogik.

## Transformationslogik

Die Sensordaten einer Flasche kommen nicht in einer einzigen Nachricht an, sondern verteilt über mehrere MQTT-Topics. Deshalb sammelt `transform.py` die eingehenden Nachrichten zunächst in einem Zwischenspeicher. Der Zwischenspeicher verwendet die `bottle`-ID als Schlüssel. Sobald alle notwendigen Informationen einer Flasche vorhanden sind, wird daraus eine vollständige Zeile erzeugt und gespeichert. Das Topic `recipe` wird über die in den Dispenser-Nachrichten enthaltene Rezept-ID pro Flasche gespeichert. Die für Regression und Klassifikation benötigten Sensordaten liegen vollständig in einer Zeile pro Flasche vor.

Gesammelt werden unter anderem:

- Füllstand der roten, blauen und grünen Station
- Vibrationsindex der roten, blauen und grünen Station
- Temperaturwerte
- Endgewicht der Flasche
- Qualitätslabel `is_cracked`
- Schwingungszeitreihe `drop_oscillation`

Da die Temperatur-Nachrichten keine eigene `bottle`-ID enthalten, werden sie über den Zeitstempel der passenden Flasche zugeordnet.

## Speicherung

Die Daten werden doppelt gespeichert:

1. als CSV-Datei `data.csv`
2. als SQLite-Datenbank `data.db`

Die SQLite-Datenbank enthält die Tabelle `flaschen`. Eine Zeile entspricht einer vollständig erfassten Flasche.

## CSV- und Datenbankstruktur

| Spalte | Bedeutung |
|------|-----------|
| `bottle` | eindeutige Flaschen-ID |
| `recipe` | Rezeptnummer |
| `fill_level_grams_red` | Füllstand an der roten Station |
| `fill_level_grams_blue` | Füllstand an der blauen Station |
| `fill_level_grams_green` | Füllstand an der grünen Station |
| `vibration_index_red` | Vibrationsindex der roten Station |
| `vibration_index_blue` | Vibrationsindex der blauen Station |
| `vibration_index_green` | Vibrationsindex der grünen Station |
| `temperature_C_red` | Temperatur an der roten Station |
| `temperature_C_blue` | Temperatur an der blauen Station |
| `temperature_C_green` | Temperatur an der grünen Station |
| `final_weight` | Endgewicht der Flasche |
| `time_scale` | Zeitstempel der Waage |
| `is_cracked` | Qualitätslabel: 0 = in Ordnung, 1 = defekt |
| `drop_oscillation` | Vibrationszeitreihe mit 500 Messpunkten |

## Visualisierung mit matplotlib

Für die Visualisierung wurde eine Zeitreihe des Endgewichts `final_weight` erstellt. 

![Zeitreihe final_weight](assets/zeitreihe_final_weight.png)

## Streamlit-Dashboard

Zusätzlich wurde ein Streamlit-Dashboard erstellt. Es zeigt Kennzahlen wie Anzahl der Flaschen, defekte Flaschen und Ausschussrate. Außerdem enthält es eine auswählbare Zeitreihe, einen Scatterplot und eine Tabelle der letzten Flaschen.

![Dashboard](dashboard.png)

Die Rohdatenansicht im Dashboard zeigt die zuletzt gespeicherten Flaschen:

![Rohdaten](rohdaten.png)

## Aufzeichnungsdauer

Die Daten wurden für deutlich länger als 15 Minuten gesammelt.

## Starten des Systems

Zuerst wird der MQTT-Subscriber gestartet:

```bash
python main.py
```

Zusätzlich kann das Streamlit-Dashboard in einem weiteren Terminal gestartet werden:

```bash
streamlit run dashboard.py
```

Für den matplotlib-Plot kann außerdem gestartet werden:

```bash
python visualisierung.py
```