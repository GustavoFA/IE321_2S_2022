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
bme = BME680_I2C(i2c=i2c)					# End: 119
display = ssd1306.SSD1306_I2C(128, 32, i2c)	# End: 60

# Configuração das GPIOs para Botão e Leds
button = Pin(22, Pin.IN, Pin.PULL_UP)
led = Pin(25, machine.Pin.OUT)
led_B = Pin(19, machine.Pin.OUT)
led_G = Pin(18, machine.Pin.OUT)
led_R = Pin(27, machine.Pin.OUT) 

led.value(0)	# não está sendo usada
led_R.value(0)
led_G.value(0)
led_B.value(1)

# Variáveis
state = 0
disp_prob = 0
relogio_oled = ticks_ms()
relogio_bme = ticks_ms()
relogio_scan = ticks_ms() 
relogio_led = ticks_ms()

# Tempo para os dispositivos iniciarem
sleep_ms(1500)


def RGB_f(end):
    if end == 60:     
        led_R.on()
        led_G.off()
    elif end == 119:
        led_R.off()
        led_G.on()
    else:
        led_R.off()
        led_G.off()


# Laço principal
while True:          
        
    
    # Leitura do botão com debounced
    if(button.value() == 0):
        sleep_ms(150)	# Debounced
        if(button.value() == 0):
            state = state + 1
            if state > 4:
                state = 0
            #print(state)            
        
    
    ''' Tentativa de impressão no OLED, se caso o mesmo não estiver conectado
    não será possível entrar no if seguinte.
    '''
    
    try:
        
        # Obtenção dos parâmetros a cada 500 ms
        if(ticks_ms() - relogio_bme > 500):
            temp = str(round(bme.temperature, 2)) + ' C'
            hum = str(round(bme.humidity, 2)) + ' %'
            pres = str(round(bme.pressure, 2)) + ' hPa'
            ar = str(round(bme.gas/1000, 2)) + ' KOhms'
            alt = str(round(bme.altitude, 2)) + ' m'
            relogio_bme = ticks_ms()
    
    
        if (ticks_ms() - relogio_oled) > 500:
            
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
                
            #if disp_prob != 0:
                #print('aqui')
                
            disp_prob = 0
            led_B(1)
            led_G(0)
            led_R(0)
            
    except:
        
    
        
        if(disp_prob == 0):
            devices = i2c.scan()
            
            if(devices[0] != 119):
                RGB_f(119)
                led_B(0)
                disp_prob = 2 
            elif(devices[0] != 60):
                RGB_f(60)
                led_B(0)
                disp_prob = 1
        elif(disp_prob == 2):
            if(ticks_ms() - relogio_led > 500):
                led_R.toggle()
                relogio_led = ticks_ms()
                '''
                devices = i2c.scan()
                if devices > 1:
                    if devices[1] == 119:
                        display = ssd1306.SSD1306_I2C(128, 32, i2c)	# End: 119
                elif devices > 0:
                    if devices[0] == 119:
                        display = ssd1306.SSD1306_I2C(128, 32, i2c)	# End: 119
                '''                    
        elif(disp_prob == 1):
            if(ticks_ms() - relogio_led > 500):
                led_G.toggle()
                relogio_led = ticks_ms()
                '''
                devices = i2c.scan()
                if devices > 1:
                    if devices[1] == 60:
                        bme = BME680_I2C(i2c=i2c)					# End: 60
                elif devices > 0:
                    if devices[0] == 60:
                        bme = BME680_I2C(i2c=i2c)					# End: 60
                '''
        
        
        

