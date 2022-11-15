"""
Código para validação do funcionamento do BME680 + OLED
Botão de chaveamento de informações do sensor
    O botão serve para chavear no display as diferentes grandezas capturadas pelo sensor:
        * Pressão Atmosférica
        * Temperatura
        * Umidade
        * Qualidade do ar
        * Altitude
LED RGB de indicação de funcionamento ou falha
    * LED em verde indica que o circuito está funcional
    * LED pisca em verde quando executa leitura do sensor
    * LED pisca em verde quando pressiona o botão
    * LED pisca em vermelho quando há falha de leitura do sensor
    * LED pisca em azul quando há falha de leitura do OLED
"""

# Bibliotecas
from machine import Pin, I2C
from bme680 import *
from time import ticks_ms, sleep_ms
import ssd1306

# Definição dos valores de on/off para LED RGB:
# Anodo comum  => on=0, off=1
# Catodo comum => on=1, off=0
LED_ON = 1
LED_OFF = 0

# Configuração I2C da Pico
# Usaremos I2C 0, GPIO 20 e 21 --> SDA e SCL
i2c = I2C(0, scl=Pin(21), sda=Pin(20))

# Inicializando e configurando a I2C dos dispositivos
bme = BME680_I2C(i2c=i2c)					# End: 119
display = ssd1306.SSD1306_I2C(128, 32, i2c)	# End: 60

# Configuração das GPIOs para Botão e Leds
button = Pin(22, Pin.IN, Pin.PULL_UP)
led = Pin(25, machine.Pin.OUT)
led_B = Pin(19, machine.Pin.OUT)
led_G = Pin(18, machine.Pin.OUT)
led_R = Pin(27, machine.Pin.OUT) 

led.value(0)	# não está sendo usada
led_R.value(LED_OFF)
led_G.value(LED_ON)
led_B.value(LED_OFF)

# Variáveis
state = 0
disp_prob = 0
relogio_oled = ticks_ms()
relogio_bme = ticks_ms()
relogio_scan = ticks_ms() 
relogio_led = ticks_ms()
button_time = ticks_ms()

# Tempo de cada conjunto de medidas (ms)
tempo_par = 500

# Tempo para os dispositivos iniciarem
sleep_ms(2000)


# Função para definir iluminação para cada situação do sistema
def RGB_f(end):
    if end == 60:     
        led_R.value(LED_OFF)
        led_G.value(LED_OFF)
        led_B.value(LED_ON)
    elif end == 119:
        led_R.value(LED_ON)
        led_G.value(LED_OFF)
        led_B.value(LED_OFF)
    else:
        led_R.value(LED_OFF)
        led_B.value(LED_OFF)


# Laço principal
while True:          
        
    
    # Leitura do botão com debounced
    if(button.value() == 0):
        # Debounced
        if(button.value() == 0) and (ticks_ms() - button_time > 150):
            button_time = ticks_ms()
            state = state + 1
            if state > 4:
                state = 0           
        
    
    try:
        
        if(disp_prob == 0):
            if(ticks_ms() - relogio_bme < 250):
                led_G.value(LED_ON)
                led_G(LED_OFF)
                led_R(LED_OFF)
            else:
                led_G.value(LED_OFF)
                led_G(LED_OFF)
                led_R(LED_OFF)
        
        # Obtenção dos parâmetros a cada 500 ms
        if(ticks_ms() - relogio_bme > tempo_par):
            temp = str(round(bme.temperature, 2)) + ' C'
            hum = str(round(bme.humidity, 2)) + ' %'
            pres = str(round(bme.pressure, 2)) + ' hPa'
            ar = str(round(bme.gas/1000, 2)) + ' KOhms'
            alt = str(round(bme.altitude, 2)) + ' m'
            relogio_bme = ticks_ms()
            disp_prob = 0
    
    
        if (ticks_ms() - relogio_oled) > 2*tempo_par:
            
            relogio_oled = ticks_ms()
        
            if(state == 0):
                display.fill(0)
                display.text('Temperatura: ', 0, 0)
                display.text(temp, 0, 24)
                display.show()
            elif(state == 1):
                display.fill(0)
                display.text('Umidade Relativa: ', 0, 0)
                display.text(hum, 0, 24)
                display.show()
            elif(state == 2):
                display.fill(0)
                display.text('Pressao: ', 0, 0)
                display.text(pres, 0, 24)
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
            
    except OSError as ose:
        
        if(disp_prob == 0):
            devices = i2c.scan()
            
            if(devices[0] != 119):
                RGB_f(119)
                disp_prob = 2 
            elif(devices[0] != 60):
                RGB_f(60)
                disp_prob = 1
        elif(disp_prob == 2):
            if(ticks_ms() - relogio_led > 500):
                led_R.toggle()
                relogio_led = ticks_ms()                   
        elif(disp_prob == 1):
            if(ticks_ms() - relogio_led > 500):
                led_B.toggle()
                relogio_led = ticks_ms()
        
    except KeyboardInterrupt as k:
        sys.exit()
    except BaseException as e:
        print(type(e))
        print(f'Unexpected {e}')
        
        

