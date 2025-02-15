from machine import ADC, Pin, PWM, Timer
import utime
import math 

maxVal=180
modeindex=0
modes=['cat','circle','centre']

class Servo:
    def __init__(self, pin: int or Pin or PWM, minVal=1000, maxVal=6500):
        if isinstance(pin, int):
            pin = Pin(pin, Pin.OUT)
        if isinstance(pin, Pin):
            self.__pwm = PWM(pin)
        if isinstance(pin, PWM):
            self.__pwm = pin
        self.__pwm.freq(50)
        self.minVal = minVal
        self.maxVal = maxVal
 
    def deinit(self):
        self.__pwm.deinit()
 
    def sMap(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def goto(self, angle: int):
        value=round(self.sMap(max(0,min(180,angle)),0,180,0,maxVal))
        delta = self.maxVal-self.minVal
        target = int(self.minVal + ((max(0,min(maxVal,value)) / maxVal) * delta))
        self.__pwm.duty_u16(target) #/65025
 
    def free(self):
        self.__pwm.duty_u16(0)

def on_pressed(timer):
    global modeindex
    #laser.toggle()
    modeindex=(modeindex+1)%len(modes)
    print('button')

def debounce(pin):
    # Start or replace a timer for 200ms, and trigger on_pressed.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed)

servoInt = Servo(0)#GP0  
servoExt = Servo(2)#GP2

laser=Pin(17, Pin.OUT) #gp17
switch = Pin(14, Pin.IN, Pin.PULL_UP) #gp14 switch.value()
timer = Timer(-1) #virtual timer only supported (-1)
switch.irq(debounce, Pin.IRQ_RISING)
    
laser.value(True)
i=0

while True:
    if modes[modeindex]=='circle':
        i=(i+10)%360
        servoInt.goto(90+20*math.sin(i/360*2*math.pi))
        servoExt.goto(90+20*math.cos(i/360*2*math.pi))
        #laser.toggle()
        utime.sleep(0.05)
    if modes[modeindex]=='cat':
        i=(i+2)%360
        servoInt.goto(90+20*math.sin(3*i/360*2*math.pi))
        servoExt.goto(150+10*math.cos(i/360*2*math.pi))
        #laser.value(i%20!=0)
        utime.sleep(0.05)
    if modes[modeindex]=='sweep':
        for i in range(45,90+45,10):
            servoInt.goto(i)
            servoExt.goto(i)
            utime.sleep(0.05)
            if modes[modeindex]!='sweep': break
        for i in range(90+45,45,-10):
            servoInt.goto(i)
            servoExt.goto(i)
            utime.sleep(0.05)
            if modes[modeindex]!='sweep': break
    if  modes[modeindex]=='centre':
        servoInt.goto(90)
        servoExt.goto(90)
    #laser.toggle()
    #print(switch.value())
        
    




