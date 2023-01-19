# some parts of the startup may be a bit sloppy and can/will be improved later on!

from hcsr04 import HCSR04
from umqttsimple import MQTTClient
from src.wifi_manager import WifiManager
import settings
from ubinascii import hexlify
from machine import unique_id
from machine import Pin, ADC, SoftI2C
import ssd1306

wm = WifiManager(ssid=settings.ssid, password=settings.password)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(settings.oled_width, settings.oled_height, i2c)
client_id = hexlify(unique_id())
distance_sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
moisture_sensor = ADC(Pin(34))
moisture_sensor.atten(ADC.ATTN_11DB)
client = MQTTClient(client_id, settings.mqtt_broker)