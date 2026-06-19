import paho.mqtt.client as mqtt
import json

BROKER = "158.180.44.197"
PORT   = 1883
TOPIC  = "aut/SoSe26/learning_factory_simulation/#"

def start(on_message_callback):
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"[MQTT] Verbunden (code={reason_code})")
        client.subscribe(TOPIC, qos=0)

    def on_message(client, userdata, message):
        parts = message.topic.split("/")
        # letzten Teil als Typ, Sonderfall scale/final_weight
        if len(parts) >= 2 and parts[-2] == "scale":
            topic_type = "final_weight"
        else:
            topic_type = parts[-1]

        try:
            payload = json.loads(message.payload.decode("utf-8"))
        except json.JSONDecodeError:
            print(f"[MQTT] JSON-Fehler bei Topic {message.topic}")
            return

        on_message_callback(topic_type, payload)

    def on_disconnect(client, userdata, flags, reason_code, properties):
        print(f"[MQTT] Verbindung getrennt (code={reason_code}), versuche neu...")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set("bobm", "letmein")
    client.on_connect    = on_connect
    client.on_message    = on_message
    client.on_disconnect = on_disconnect
    client.connect(BROKER, PORT)
    client.loop_start()
    return client