printf "Hello! this script will try to get and install everything you need to get you running!\n"
printf "There is no error handling yet, so the script might fail.\n"
read -p "Press any key to continue"
printf "I will assume that curl, python and pip are installed. \nplease make sure that these dependencies are met :)\n"
echo -e "Take a look at this link: https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/"
echo -e "Follow the instructions and come back once the firmware is installed on your device..."
read -p "Press any key to continue"
echo "Great!"
echo "We will now try to install a tool, to upload the code to the ESP!"
sleep 4
pip3 install --user adafruit-ampy
echo "Wonderful!"
echo "Now we will try to apply some settings!"
read -p "please enter the hostname or IP of your MQTT-broker: " broker
read -p "set the initial SSID for your access point: " ssid
read -p "set the password for your access point: " password
read -p "set the width of the OLED display in pixels: " width
read -p "set the height of the display: " height
read -p "set the line height of your display, usually 10: " line
echo "please calibrate your moisture sensor!"
read -p "set the value when put in air: " dry
read -p "set the value when put in water: " wet
read -p "what's the height of your pot in mm?: " pot_height
read -p "with what name should this device be identified?: " name
read -p "how often do you want your device to publish data (in seconds)?: " refresh
printf "
mqtt_broker = '${broker}'
topic = 'plants'
ssid = '${ssid}'
password = '${password}'
oled_width = ${width}
oled_height = ${height}
moisture_dry = ${dry}
moisture_wet = ${wet}
line_height = ${line}
pot_height_in_mm = ${pot_height}
client_name = '${name}'
refresh_interval_in_seconds = ${refresh} \n" > ${BASH_SOURCE%/*}/src/settings.py
echo"Coolio. Will now try to upload project to the device..."
read -p "press enter to continue"
ampy --port /dev/ttyUSB0 put ${BASH_SOURCE%/*}/src
sleep 3
echo "if everything worked, the device should start up now..."
