import sys
from utime import sleep

import machine
from machine import reset

import settings
from boot import display, wm, client_id, moisture_sensor, distance_sensor, client
from settings import line_height, client_name as identifier, refresh_interval_in_seconds as refresh_interval
from umqttsimple import MQTTException
import _thread

lock = _thread.allocate_lock()


def get_moisture_percent(raw_value: int):
    air_val = settings.moisture_dry
    water_val = settings.moisture_wet
    max_diff = air_val - water_val
    return 1 - (raw_value - water_val) / float(max_diff)


def sub_cb(topic, msg):
    print((topic, msg))
    if topic == settings.topic and msg == b'received':
        print('ESP received message')


def publish_data():
    while True:
        lock.acquire()
        display.fill(0)
        if not wm.is_connected():
            reconnect()
        display.fill(0)
        display.text("publishing...", 0, 0)
        display.show()
        current_moisture = get_moisture_percent(moisture_sensor.read_u16())
        current_height = round(distance_sensor.distance_mm() - settings.pot_height_in_mm, 2)
        try:
            client.publish(
                settings.topic,
                f"plants,identifier={identifier} height={current_height},moisture={current_moisture}"
            )
            display.text("SUCCESS!", 0, line_height)

        except AssertionError:
            display.text("FAILED!", 0, line_height)

        finally:
            display.show()
            sleep(5)
            lock.release()
            client.disconnect()
            wm.disconnect()
            sleep(refresh_interval)


def monitor():
    display.fill(0)
    _thread.start_new_thread(publish_data, ())

    while True:
        lock.acquire()
        display.fill(0)
        print(moisture_sensor.read_u16())
        current_moisture = get_moisture_percent(moisture_sensor.read_u16())
        current_height = round(distance_sensor.distance_mm() - settings.pot_height_in_mm, 2)
        display.text("soil moisture: ", 0, 0)
        display.text(f"{round(current_moisture * 100, 2)} %", 0, line_height)
        display.text("current height:", 0, 3 * line_height)
        display.text(f"{current_height / 10} cm", 0, 4 * line_height)
        display.show()
        lock.release()
        sleep(20)


def setup_wifi():
    try:
        display.fill(0)
        display.text("web:", 0, 0)
        display.text(wm.wlan_ap.ifconfig()[0], 0, line_height)  # IP address with which it can be accessed
        display.text("SSID: ", 0, 2 * line_height)
        display.text(settings.ssid, 0, 3 * line_height)
        display.text("password:", 0, 4 * line_height)
        display.text(settings.password, 0, 5 * line_height)
        display.show()
        wm.connect()

    except KeyboardInterrupt:
        sys.exit()

    except:
        display.fill(0)
        display.text("something went wrong...", 0, 0)
        display.text("device will restart.", 0, line_height)
        display.text("if error persists,", 0, 2 * line_height)
        display.text(" flash device.", 0, 3 * line_height)
        display.show()
        sleep(10)
        reset()

    display.fill(0)
    display.text("Success!", 0, 0)
    connection = wm.get_address()[0]
    display.text("current IP:", 0, 2 * line_height)
    display.text(connection, 0, 3 * line_height)
    display.show()
    sleep(10)


def setup_mqtt():
    display.fill(0)
    display.text("SETTING UP MQTT", 0, 0)
    display.text("broker address:", 0, 2 * line_height)
    display.text(client.server, 0, 3 * line_height)
    display.text("My ClientID:", 0, 4 * line_height)
    display.text(client.client_id, 0, 5 * line_height)
    display.show()
    sleep(10)
    display.fill(0)
    display.text("CONNECTING...", 0, 0)
    display.show()
    try:
        client.set_callback(sub_cb)
        client.connect()
        client.subscribe(settings.topic)

    except MQTTException:
        display.text("ERROR", 0, 2 * line_height)
        display.text("NOW RESTARTING...", 0, 3 * line_height)
        display.show()
        sleep(10)
        reset()

    display.text("Success!", 0, 20)
    display.show()
    sleep(3)


def initial_setup():
    setup_wifi()
    setup_mqtt()


def reconnect():
    display.fill(0)
    display.text("reconnecting...", 0, 0)
    display.show()
    try:
        wm.connect()
        display.text("Success!", 0, line_height)
        sleep(1)
        display.text("Connecting to Broker...", 0, 2 * line_height)
        display.show()
        client.set_callback(sub_cb)
        client.connect()
        client.subscribe(settings.topic)
        display.text("Success!", 0, 3 * line_height)

    except:
        display.fill(0)
        display.text("Error!!", 0, line_height)
        display.text("If issue persists,", 0, 2 * line_height)
        display.text("flash device again.", 0, 3 * line_height)
    finally:
        display.show()
        sleep(4)


initial_setup()
monitor()

