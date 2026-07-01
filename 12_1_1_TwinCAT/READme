# Aufgabe 12.1.1 – TwinCAT MQTT-Client

## Ziel der Aufgabe

In dieser Aufgabe wurde das bestehende TwinCAT-Programm um einen MQTT-Client erweitert.  
Die SPS veröffentlicht Sensordaten der Learning Factory regelmäßig an den MQTT-Broker.

Dabei werden statische Informationen wie Gruppenname, Namen der Gruppenmitglieder und Einheiten einmalig beim Start gesendet. Die Messwerte der Sensoren werden anschließend periodisch alle 10 Sekunden veröffentlicht.

Alle MQTT-Nachrichten werden mit `Retain = TRUE` gesendet, damit die aktuellen Werte auch für neue Subscriber direkt sichtbar sind.

## Verwendete TwinCAT-Komponenten

Für die MQTT-Kommunikation wurde die TwinCAT-IoT-Bibliothek verwendet.

| Komponente | Verwendung |
|---|---|
| `TF6701 TwinCAT 3 IoT Communication` | Paket für MQTT-Kommunikation |
| `Tc3_IotBase` | TwinCAT-Library mit `FB_IotMqttClient` |
| `FB_IotMqttClient` | MQTT-Client in der SPS |
| `TON` | Timer für das 10-Sekunden-Sendeintervall |

## MQTT-Broker

Die SPS verbindet sich mit dem vorgegebenen MQTT-Broker:

| Einstellung | Wert |
|---|---|
| Broker | `158.180.44.197` |
| Port | `1883` |
| Benutzer | `bobm` |
| Passwort | `letmein` |

## Topic-Struktur

Als Topic-Präfix wird verwendet:

```text
aut/SoSe26/SiJuLe/
```