import time

import mqtt_client
import transform
import database

def on_message(topic_type, payload):
    transform.handle(topic_type, payload, database.save)

if __name__ == "__main__":
    client = mqtt_client.start(on_message)
    print("System läuft. Strg+C zum Beenden.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBeende...")
        client.loop_stop()
        client.disconnect()