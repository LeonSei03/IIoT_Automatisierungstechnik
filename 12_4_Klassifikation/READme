# Aufgabe 12.4 – Klassifikationsmodell

## Ziel der Aufgabe

In dieser Aufgabe wurde ein Klassifikationsmodell mit `scikit-learn` trainiert. Ziel war es, defekte Flaschen anhand der Vibrationszeitreihe `drop_oscillation` zu erkennen.

Die Zielgröße des Modells ist:

| Größe | Beschreibung |
|---|---|
| `is_cracked` | Qualitätslabel der Flasche: `0` = intakt, `1` = defekt |

Für diese Aufgabe wurde keine Prognose-CSV benötigt. Stattdessen sollten Feature Engineering, eine Confusion Matrix und F1-Scores für verschiedene Feature-Kombinationen dokumentiert werden.

## Dateien

| Datei | Beschreibung |
|---|---|
| `classification.ipynb` | Notebook zum Feature Engineering, Training und zur Auswertung |
| `data.csv` | Datensatz mit Flaschendaten, `drop_oscillation` und Zielwert `is_cracked` |
| `classification_feature_results.csv` | Ergebnistabelle mit Feature-Kombinationen, Modell und F1-Score |
| `confusion_matrix.png` | Confusion Matrix des besten Modells |

## Datenbasis

Als Eingabedaten wurde die Datei `data.csv` verwendet. Die Spalte `drop_oscillation` enthält pro Flasche eine Schwingungszeitreihe mit 500 Messpunkten.

Die Werte sind als String gespeicherte Liste abgelegt und werden im Notebook mit `ast.literal_eval()` wieder in eine Python-Liste umgewandelt.

## Feature Engineering

Aus der Vibrationszeitreihe `drop_oscillation` wurden statistische Merkmale berechnet. Dadurch wird jede Zeitreihe mit 500 Messpunkten auf mehrere numerische Kennwerte reduziert.

Verwendete Features:

| Feature | Bedeutung |
|---|---|
| `rms` | Root Mean Square der Schwingung |
| `mean` | Mittelwert |
| `std` | Standardabweichung |
| `min` | kleinster Wert der Zeitreihe |
| `max` | größter Wert der Zeitreihe |
| `range` | Spannweite zwischen Maximum und Minimum |
| `median` | Median der Zeitreihe |

## Modelle

Es wurden verschiedene Klassifikationsmodelle getestet:

| Modell | Beschreibung |
|---|---|
| kNN | k-Nearest-Neighbors-Klassifikator |
| Log. Regression | Logistische Regression |
| Decision Tree | Entscheidungsbaum |

Die Modelle wurden mit verschiedenen Feature-Kombinationen trainiert und anhand des F1-Scores bewertet.

## Ergebnisse

| Features | Modell | F1 Training | F1 Test |
|---|---|---:|---:|
| `rms` | kNN | 0.7342 | 0.5000 |
| `rms` | Log. Regression | 0.0000 | 0.0000 |
| `rms` | Decision Tree | 0.8205 | 0.5217 |
| `mean, std` | kNN | 0.6377 | 0.5714 |
| `mean, std` | Log. Regression | 0.0000 | 0.0000 |
| `mean, std` | Decision Tree | 0.8354 | 0.6400 |
| `min, max, range` | kNN | 0.2857 | 0.0000 |
| `min, max, range` | Log. Regression | 0.0000 | 0.0000 |
| `min, max, range` | Decision Tree | 0.5490 | 0.2353 |
| `rms, mean, std` | kNN | 0.6765 | 0.5455 |
| `rms, mean, std` | Log. Regression | 0.0000 | 0.0000 |
| `rms, mean, std` | Decision Tree | 0.8354 | 0.5833 |
| `rms, mean, std, min, max` | kNN | 0.4255 | 0.1429 |
| `rms, mean, std, min, max` | Log. Regression | 0.0000 | 0.0000 |
| `rms, mean, std, min, max` | Decision Tree | 0.8438 | 0.2857 |
| alle statistischen Features | kNN | 0.3333 | 0.3333 |
| alle statistischen Features | Log. Regression | 0.0000 | 0.0000 |
| alle statistischen Features | Decision Tree | 0.8136 | 0.1667 |

Das beste Ergebnis auf den Testdaten wurde mit folgendem Modell erreicht:

| Eigenschaft | Wert |
|---|---|
| Features | `mean`, `std` |
| Modell | Decision Tree |
| F1-Score Test | 0.6400 |

## Confusion Matrix

Die folgende Confusion Matrix zeigt die Auswertung des besten Modells auf den Testdaten.

![Confusion Matrix](confusion_matrix.png)

| | Vorhergesagt intakt | Vorhergesagt defekt |
|---|---:|---:|
| Tatsächlich intakt | 111 | 7 |
| Tatsächlich defekt | 2 | 8 |

Das Modell erkennt 8 von 10 defekten Flaschen korrekt. Zwei defekte Flaschen wurden fälschlicherweise als intakt klassifiziert. Zusätzlich wurden sieben intakte Flaschen fälschlicherweise als defekt erkannt.

## Bewertung

Die logistische Regression erreicht in dieser Auswertung einen F1-Score von 0. Dies deutet darauf hin, dass sie die defekte Klasse in diesem Datensatz nicht sinnvoll erkennt. Das liegt vermutlich auch an der ungleichen Verteilung zwischen intakten und defekten Flaschen.

Der Decision Tree liefert mit den Features `mean` und `std` das beste Testergebnis. Diese beiden Merkmale reichen in diesem Datensatz aus, um Unterschiede zwischen intakten und defekten Flaschen vergleichsweise gut zu erkennen.
