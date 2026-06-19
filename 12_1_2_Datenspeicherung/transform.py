
# Sammelt alle Topics einer Flasche und gibt eine fertige Zeile zurück
_buffer = {}   # bottle-ID -> dict mit allen Feldern

# Welche Felder brauchen wir mindestens, bevor wir speichern?
_REQUIRED = {
    "dispenser_red", "dispenser_blue", "dispenser_green",
    "temp_red", "temp_blue", "temp_green",
    "final_weight", "drop_oscillation", "ground_truth"
}

def handle(topic_type, payload, save_callback):
    """
    Wird fuer jede eingehende Nachricht aufgerufen.
    Wenn eine Flasche komplett ist, wird save_callback(row_dict) aufgerufen.
    """

    # recipe ist flaschenunabhaengig, global merken
    if topic_type == "recipe":
        handle._recipe = payload
        return

    recipe = getattr(handle, "_recipe", None)

    # Dispenser-Nachrichten (red / blue / green)
    if topic_type in ("dispenser_red", "dispenser_blue", "dispenser_green"):
        color  = payload["dispenser"]          # "red", "blue", "green"
        bottle = payload["bottle"]
        _ensure(bottle)
        b = _buffer[bottle]
        b[f"fill_level_grams_{color}"]  = payload["fill_level_grams"]
        b[f"vibration_index_{color}"]   = payload["vibration-index"]
        b[f"time_{color}"]              = payload["time"]
        b[f"recipe"]                    = payload["recipe"]
        b["_got"].add(f"dispenser_{color}")

    # Temperatur (nur dispenser + time, keine bottle-ID)
    elif topic_type == "temperature":
        color = payload["dispenser"]
        t     = payload["time"]
        # Flasche ueber Zeitstempel suchen (naechster passender)
        bottle = _find_bottle_by_time(t, color)
        if bottle:
            _buffer[bottle][f"temperature_C_{color}"] = payload["temperature_C"]
            _buffer[bottle]["_got"].add(f"temp_{color}")

    # Endgewicht 
    elif topic_type == "final_weight":
        bottle = payload["bottle"]
        _ensure(bottle)
        _buffer[bottle]["final_weight"] = payload["final_weight"]
        _buffer[bottle]["time_scale"]   = payload["time"]
        _buffer[bottle]["_got"].add("final_weight")

    # Schwingung (500 Werte als Liste)
    elif topic_type == "drop_oscillation":
        bottle = payload["bottle"]
        _ensure(bottle)
        _buffer[bottle]["drop_oscillation"] = payload["drop_oscillation"]
        _buffer[bottle]["_got"].add("drop_oscillation")

    # Ground Truth (kommt als letztes)
    elif topic_type == "ground_truth":
        bottle = payload["bottle"]
        _ensure(bottle)
        _buffer[bottle]["is_cracked"] = int(payload["is_cracked"])
        _buffer[bottle]["_got"].add("ground_truth")

    # Komplett? Dann speichern
    if topic_type == "ground_truth" and payload["bottle"] in _buffer:
        bottle = payload["bottle"]
        b = _buffer[bottle]
        if _REQUIRED.issubset(b["_got"]):
            row = _build_row(bottle, b)
            save_callback(row)
            del _buffer[bottle]   # Speicher freigeben


# ein paar Hilfsfunktionen
def _ensure(bottle):
    if bottle not in _buffer:
        _buffer[bottle] = {"bottle": bottle, "_got": set()}

def _find_bottle_by_time(t, color):
    """Sucht die Flasche, deren dispenser_<color>-Zeit am naechsten an t liegt."""
    best_bottle = None
    best_diff   = float("inf")
    time_key    = f"time_{color}"
    for bottle, data in _buffer.items():
        if time_key in data:
            diff = abs(data[time_key] - t)
            if diff < best_diff and diff < 5:   # max 5 Sekunden Toleranz
                best_diff   = diff
                best_bottle = bottle
    return best_bottle

def _build_row(bottle, b):
    return {
        "bottle":                  bottle,
        "recipe":                  b.get("recipe"),
        # Rot
        "fill_level_grams_red":    b.get("fill_level_grams_red"),
        "vibration_index_red":     b.get("vibration_index_red"),
        "time_red":                b.get("time_red"),
        "temperature_C_red":       b.get("temperature_C_red"),
        # Blau
        "fill_level_grams_blue":   b.get("fill_level_grams_blue"),
        "vibration_index_blue":    b.get("vibration_index_blue"),
        "time_blue":               b.get("time_blue"),
        "temperature_C_blue":      b.get("temperature_C_blue"),
        # Grün
        "fill_level_grams_green":  b.get("fill_level_grams_green"),
        "vibration_index_green":   b.get("vibration_index_green"),
        "time_green":              b.get("time_green"),
        "temperature_C_green":     b.get("temperature_C_green"),
        # Waage + Qualität
        "final_weight":            b.get("final_weight"),
        "time_scale":              b.get("time_scale"),
        "is_cracked":              b.get("is_cracked"),
        # Schwingung (als JSON-String gespeichert)
        "drop_oscillation":        str(b.get("drop_oscillation", [])),
    }