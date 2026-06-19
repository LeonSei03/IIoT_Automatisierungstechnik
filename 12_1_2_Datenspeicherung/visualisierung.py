import os
import time
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
SPALTE   = "final_weight" # je nachdem was wir plotten wollen
INTERVALL = 5 # Sekunden zwischen Updates

plt.ion()
fig, ax = plt.subplots(figsize=(10, 4))

while True:
    try:
        df = pd.read_csv(CSV_PATH)
        ax.clear()
        ax.plot(df.index, df[SPALTE], marker="o", markersize=3, linewidth=1)
        ax.set_title(f"Live-Plot: {SPALTE}  ({len(df)} Flaschen)")
        ax.set_xlabel("Flasche (Index)")
        ax.set_ylabel(SPALTE)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.pause(0.1)
    except FileNotFoundError:
        print("CSV noch nicht vorhanden, warte...")
    except Exception as e:
        print(f"Fehler: {e}")

    time.sleep(INTERVALL)