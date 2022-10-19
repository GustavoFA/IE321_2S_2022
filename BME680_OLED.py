# Código para validação do funcionamento do BME680 + OLED

from machine import Pin, I2C
from bme680 import *
from time import sleep
import ssd1306

i2c = I2C(0, scl=Pin(21), sda=Pin(20))
bme = BME680_I2C(i2c=i2c)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

button = Pin(22, Pin.IN, Pin.PULL_UP)
led = Pin(25, machine.Pin.OUT)

state = 0


while True:
    
    if(button.value() == 0):
        state = state + 1
    if state > 4:
        state = 0
    
    sleep(0.25)
    
    led.on()
  
    temp = str(round(bme.temperature, 2)) + ' C'
    hum = str(round(bme.humidity, 2)) + ' %'
    pres = str(round(bme.pressure, 2)) + ' hPa'
    gas = str(round(bme.gas/1000, 2)) + ' KOhms'
    alt = str(round(bme.altitude, 2)) + ' m'
    
    if(state == 0):
        #print(temp)
        display.fill(0)
        display.text('T: '+temp, 0, 24)
        display.show()
    elif(state == 1):
        #print(hum)
        display.fill(0)
        display.text('H: '+hum, 0, 24)
        display.show()
    elif(state == 2):
        #print(pres)
        display.fill(0)
        display.text('P: '+pres, 0, 24)
        display.show()
    elif(state == 3):
        display.fill(0)
        display.text('A: '+alt, 0, 24)
        display.show()
    else:
        #print(gas)
        display.fill(0)
        display.text('G: '+gas, 0, 24)
        display.show()
    
    led.off()
    
    sleep(0.25)
