import os
import logging
import threading
from datetime import datetime
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)

client_id = "blinky"
mqtt_host = os.getenv("MQTT_HOST")
mqtt_port = int(os.getenv("MQTT_PORT"))
mqtt_user = os.getenv("MQTT_USER")
mqtt_pass = os.getenv("MQTT_PASS")


def on_connect(client, userdata, flags, reason_code, properties=None):
    logging.info("on_connect: {}".format(mqtt.connack_string(reason_code)))
    client.publish(
        "health/" + client._client_id.decode("utf-8"),
        payload="connected",
        retain=True,
        qos=1,
    )


def on_disconnect(client, userdata, reason_code, properties=None):
    logging.info("on_disconnect: {}".format(mqtt.error_string(reason_code)))


client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
client.enable_logger(logging.getLogger(__name__))

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.will_set("health/" + client_id, payload="lost", retain=True, qos=1)
client.username_pw_set(mqtt_user, mqtt_pass)
client.connect(mqtt_host, mqtt_port)

client.loop_start()

on_off = 0

WAIT_TIME_SECONDS = 1
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    on_off = 1 - on_off # toggle
    client.publish("revpi0000/set/core.a1red", payload=on_off, retain=True, qos=1)
    client.publish("revpi0000/set/core.a2green", payload=(1-on_off), retain=True, qos=1)
