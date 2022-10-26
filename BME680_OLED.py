# Código para validação do funcionamento do BME680 + OLED

# Bibliotecas
from machine import Pin, I2C
from bme680 import *
from time import ticks_ms, sleep_ms
import ssd1306

# Configuração I2C da Pico
# Usaremos I2C 0, GPIO 20 e 21 --> SDA e SCL
i2c = I2C(0, scl=Pin(21), sda=Pin(20))

# Inicializando e configurando a I2C dos dispositivos
bme = BME680_I2C(i2c=i2c)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configuração das GPIOs para Botão e Leds
button = Pin(28, Pin.IN, Pin.PULL_UP)
#led = Pin(25, Pin.OUT)
led_R = Pin(19, Pin.OUT)
led_G = Pin(18, Pin.OUT)
led_B = Pin(17, Pin.OUT)

#led.value(0)
# turning off led rgb
led_R.value(1)
led_G.value(0)
led_B.value(1)

# Variáveis
state = -1
disp_prob = 0
relogio_oled = ticks_ms()
relogio_bme = ticks_ms()
relogio_scan = ticks_ms()
relogio_led = ticks_ms()

def blink_alert():
    led_R.value(1)
    sleep_ms(400)
    led_R.toggle()

def blink_functional():
    led_G.value(1)
    sleep_ms(200)
    led_G.toggle()

def check_device_alert(device_id):
    if device_id == 60:
        blink_alert()
#     elif end == 119:
#         led_R.off()
#         led_G.on()
    else:
        led_R.value(1)
        led_G.value(1)
        led_B.value(1)

def set_error_state():
    led_G.value(1)
    led_R.value(0)

def set_normal_state():
    led_G.value(0)
    led_R.value(1)

# Laço principal
while True:
    """
    LED em verde indica que o circuito está funcional
    LED pisca em verde quando executa leitura do sensor

    """
    set_normal_state()

    # Verificação dos dispositivos conectados a cada 10 s
    if(ticks_ms() - relogio_scan > 10000):
        relogio_scan = ticks_ms()


    # Leitura do botão com debounced
    if(button.value() == 0):
        sleep_ms(150)	# Debounced
        if(button.value() == 0):
            state = state + 1
            if state > 4:
                state = 0
            blink_functional()
            print(f'button state: {state}')

    ''' Tentativa de impressão no OLED, se caso o mesmo não estiver conectado
    não será possível entrar no if seguinte.
    '''
    try:
        diff = ticks_ms() - relogio_bme
        print(diff)
        # Obtenção dos parâmetros a cada 500 ms
        if(diff > 10000):
            print('reading data')
            blink_functional()
            f_temperature = "%0.1f C" % bme.temperature
            f_humidity = "%0.1f %%" % bme.humidity
            f_pressure = "%0.3f hPa" % bme.pressure
            temp = str(round(bme.temperature, 2)) + ' C'
            print(f'\nTemperatura: {f_temperature}')
            hum = str(round(bme.humidity, 2)) + ' %'
            print(f'Umidade: {f_humidity}')
            pres = str(round(bme.pressure, 2)) + ' hPa'
            print(f'Pressão: {f_pressure}\n')
            ar = str(round(bme.gas/1000, 2)) + ' KOhms'
            alt = str(round(bme.altitude, 2)) + ' m'
            relogio_bme = ticks_ms()

#         if (ticks_ms() - relogio_oled) > 500:
#         relogio_oled = ticks_ms()
        if(state == 0):
            display.fill(0)
            display.text('Pressao: ', 0, 0)
            display.text(pres, 0, 24)
            display.show()
        elif(state == 1):
            display.fill(0)
            display.text('Temperatura: ', 0, 0)
            display.text(temp, 0, 24)
            display.show()
        elif(state == 2):
            display.fill(0)
            display.text('Umidade Relativa: ', 0, 0)
            display.text(hum, 0, 24)
            display.show()
        elif(state == 3):
            display.fill(0)
            display.text('Altitude: ', 0, 0)
            display.text(alt, 0, 24)
            display.show()
        elif(state == 4):
            display.fill(0)
            display.text('Qualidade do Ar: ', 0, 0)
            display.text(ar, 0, 24)
            display.show()
        disp_prob = 0
        if disp_prob != 0:
            check_device_alert(0)
        led_G.value(0)
        sleep_ms(500)
    except OSError as ose:
        set_error_state()
        print(f'OSError: {ose}')
        if(disp_prob == 0):
            devices = i2c.scan()
            print(f'Devices found: {devices}')
            if(devices[0] != 60):
                check_device_alert(60)
                disp_prob = 1
        elif(disp_prob == 1):
            if(ticks_ms() - relogio_led > 500):
                check_device_alert(60)
                relogio_led = ticks_ms()
        sleep_ms(5000)
    except BaseException as e:
        print(type(e))
        print(f'Unexpected {e}')



