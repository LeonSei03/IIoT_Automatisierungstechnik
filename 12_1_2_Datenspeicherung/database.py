import csv
import os
import sqlite3

CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
DB_PATH  = os.path.join(os.path.dirname(__file__), "data.db")

COLUMNS = [
    "bottle", "recipe",
    "fill_level_grams_red",  "vibration_index_red",  "time_red",  "temperature_C_red",
    "fill_level_grams_blue", "vibration_index_blue", "time_blue", "temperature_C_blue",
    "fill_level_grams_green","vibration_index_green","time_green","temperature_C_green",
    "final_weight", "time_scale", "is_cracked",
    "drop_oscillation",
]

def _init_db():
    """Legt die Tabelle an falls sie noch nicht existiert."""
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS flaschen (
            bottle               TEXT PRIMARY KEY,
            recipe               INTEGER,
            fill_level_grams_red  REAL,
            vibration_index_red   REAL,
            time_red              INTEGER,
            temperature_C_red     REAL,
            fill_level_grams_blue  REAL,
            vibration_index_blue   REAL,
            time_blue              INTEGER,
            temperature_C_blue     REAL,
            fill_level_grams_green REAL,
            vibration_index_green  REAL,
            time_green             INTEGER,
            temperature_C_green    REAL,
            final_weight          REAL,
            time_scale            INTEGER,
            is_cracked            INTEGER,
            drop_oscillation      TEXT
        )
    """)
    con.commit()
    con.close()

_init_db()

def save(row: dict):
    # CSV 
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    # SQLite
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        INSERT OR REPLACE INTO flaschen VALUES (
            :bottle, :recipe,
            :fill_level_grams_red,  :vibration_index_red,  :time_red,  :temperature_C_red,
            :fill_level_grams_blue, :vibration_index_blue, :time_blue, :temperature_C_blue,
            :fill_level_grams_green,:vibration_index_green,:time_green,:temperature_C_green,
            :final_weight, :time_scale, :is_cracked,
            :drop_oscillation
        )
    """, row)
    con.commit()
    con.close()

    print(f"[DB] Gespeichert: Flasche {row['bottle']} | is_cracked={row['is_cracked']}")