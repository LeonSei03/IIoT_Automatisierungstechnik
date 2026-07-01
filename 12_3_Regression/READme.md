# Aufgabe 12.3 – Regressionsmodell

## Ziel der Aufgabe

In dieser Aufgabe wurde ein lineares Regressionsmodell mit `scikit-learn` trainiert. Ziel war es, das Endgewicht einer Flasche anhand der aufgenommenen Sensordaten vorherzusagen.

Die Zielgröße des Modells ist:

| Größe | Beschreibung |
|------|--------------|
| `final_weight` | Endgewicht der Flasche |

Als Trainingsdaten wurde die zuvor gespeicherte `data.csv` aus Aufgabe 12.1.2 verwendet. Anschließend wurde das trainierte Modell auf den bereitgestellten Datensatz `X.csv` angewendet. Die Prognosewerte wurden in `reg_SiJuLe.csv` gespeichert.

## Dateien

| Datei | Beschreibung |
|------|--------------|
| `regression.ipynb` | Notebook zum Trainieren und Auswerten des Regressionsmodells |
| `data.csv` | Trainingsdaten mit Sensordaten und Zielwert `final_weight` |
| `X.csv` | Datensatz, auf den das trainierte Modell angewendet wurde |
| `reg_SiJuLe.csv` | Ergebnisdatei mit den vorhergesagten Endgewichten |
| `regression_feature_results.csv` | Tabelle mit Feature-Kombinationen, Zielgröße, MSE und R² |

Die verpflichtende Prognosedatei für die Abgabe ist `reg_SiJuLe.csv`. Zusätzlich wurde `regression_feature_results.csv` erzeugt, um die geforderten MSE- und R²-Werte pro Feature-Kombination nachvollziehbar zu dokumentieren.

## Datenvorbereitung

Die Trainingsdaten stammen aus der Datenspeicherung der vorherigen Aufgabe. In dieser Datei heißen die Temperaturspalten ursprünglich:

- `temperature_C_red`
- `temperature_C_blue`
- `temperature_C_green`

Da der Prognosedatensatz `X.csv` die Temperaturspalten ohne `_C_` verwendet, werden die Spalten im Notebook umbenannt:

| Ursprünglicher Name in `data.csv` | Name im Regressionsmodell |
|---|---|
| `temperature_C_red` | `temperature_red` |
| `temperature_C_blue` | `temperature_blue` |
| `temperature_C_green` | `temperature_green` |

Dadurch können Trainingsdaten und Prognosedaten mit denselben Feature-Namen verarbeitet werden.

## Modell

Als Modell wurde eine lineare Regression verwendet:

| Eigenschaft | Wert |
|---|---|
| Modelltyp | Lineare Regression |
| Bibliothek | `scikit-learn` |
| Zielgröße `y` | `final_weight` |
| Trainings-/Testsplit | 80 % Training, 20 % Test |
| Reproduzierbarkeit | `random_state=42` |

## Genutzte Features und Ergebnisse

Für verschiedene Feature-Kombinationen wurden jeweils MSE und R² berechnet.

| Features (X) | Zielgröße (y) | Modell | MSE Train | MSE Test | R² Train | R² Test |
|---|---|---|---:|---:|---:|---:|
| `fill_level_grams_red` | `final_weight` | Linear | 50.2053 | 76.0945 | 0.0015 | -0.0536 |
| `fill_level_grams_red`, `vibration_index_red` | `final_weight` | Linear | 46.1835 | 72.8148 | 0.0814 | -0.0082 |
| `fill_level_grams_red`, `vibration_index_red`, `temperature_red` | `final_weight` | Linear | 46.1195 | 72.4314 | 0.0827 | -0.0029 |
| `fill_level_grams_red`, `fill_level_grams_blue`, `fill_level_grams_green` | `final_weight` | Linear | 36.7725 | 45.9881 | 0.2686 | 0.3633 |
| `fill_level_grams_red`, `fill_level_grams_blue`, `fill_level_grams_green`, `vibration_index_red`, `vibration_index_blue`, `vibration_index_green` | `final_weight` | Linear | 0.1185 | 0.1369 | 0.9976 | 0.9981 |
| `fill_level_grams_red`, `fill_level_grams_blue`, `fill_level_grams_green`, `vibration_index_red`, `vibration_index_blue`, `vibration_index_green`, `temperature_red`, `temperature_blue`, `temperature_green` | `final_weight` | Linear | 0.0000 | 0.0000 | 1.0000 | 1.0000 |

## Bewertung der Ergebnisse

Die ersten Feature-Kombinationen mit nur wenigen Sensordaten liefern noch relativ ungenaue Vorhersagen. Besonders bei nur einem Füllstand ist der R²-Wert sehr niedrig oder sogar negativ. Das bedeutet, dass diese Feature-Kombination das Endgewicht kaum sinnvoll erklären kann.

Deutlich bessere Ergebnisse entstehen, sobald die Füllstände aller drei Stationen und die Vibrationsindizes verwendet werden. Die Kombination aus Füllständen, Vibrationsindizes und Temperaturwerten erreicht in den vorhandenen Daten die besten Werte.

Das beste Modell wurde anschließend verwendet, um die Endgewichte für den Datensatz `X.csv` vorherzusagen.

## Formel des besten Modells

Das beste Modell verwendet alle neun Sensormerkmale:

- `fill_level_grams_red`
- `fill_level_grams_blue`
- `fill_level_grams_green`
- `vibration_index_red`
- `vibration_index_blue`
- `vibration_index_green`
- `temperature_red`
- `temperature_blue`
- `temperature_green`

Die lineare Regression hat allgemein die Form:

```text
final_weight = b + w1*x1 + w2*x2 + ... + wn*xn
```

Für das beste Modell ergibt sich:

```text
final_weight =
    -15.0000
    + 0.0005 * fill_level_grams_red
    + 0.0005 * fill_level_grams_blue
    + 0.0005 * fill_level_grams_green
    + 0.1000 * vibration_index_red
    + 0.1000 * vibration_index_blue
    + 0.1000 * vibration_index_green
    + 0.2000 * temperature_red
    + 0.2000 * temperature_blue
    + 0.2000 * temperature_green
```

Die Parameter stammen aus `model.intercept_` und `model.coef_` des trainierten `LinearRegression`-Modells.



## Ergebnisdatei `reg_SiJuLe.csv`

Die Datei `reg_SiJuLe.csv` enthält die vorhergesagten Endgewichte für die Flaschen aus `X.csv`.

Die Datei enthält unter anderem:

| Spalte | Bedeutung |
|---|---|
| `Flaschen ID` | ID der Flasche aus `X.csv` |
| `y_hat` | vorhergesagtes Endgewicht |

## Ausführen des Notebooks

Das Notebook kann vollständig von oben nach unten ausgeführt werden:

1. Trainingsdaten `data.csv` laden
2. Temperaturspalten angleichen
3. Feature-Kombinationen trainieren und bewerten
4. bestes Modell auswählen
5. Prognosen für `X.csv` berechnen
6. Ergebnisse in `reg_SiJuLe.csv` speichern
