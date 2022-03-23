from machine import Pin, PWM, Signal,ADC
import utime
import time
import _thread
trigger=Pin(0,Pin.OUT)
led=Pin(25,Pin.OUT)
trigger.value(0)
#核心电压adc
vcore=ADC(2)
#1.8v电压adc
vcc18=ADC(1)
#3.3v供电开关
power33=Pin(22,Pin.OUT)
#核心电压glitch攻击
vglitch = Pin(20,Pin.OUT)

lock = _thread.allocate_lock()

START_ADC = False
glitch_times=1
vcore_list=[]
vcc18_list=[]
cmd=0
glitch_delay=0
glitch_pulse=0
#times 攻击次数、glitch_delay触发后开始攻击延时us、glitch_pulse持续拉低us
def glitch_thread(times,glitch_delay,glitch_pulse):    
    print('start')
    led.value(0)
    power33.value(1)
    while True:
        vc=vcore.read_u16()
        if vc >17000 and times >0:
            utime.sleep_us(glitch_delay)
            vglitch.value(1)
            utime.sleep_us(glitch_pulse)
            vglitch.value(0)
            times=times-1

    


while True:
    cmd=input()
    if cmd=="CMD_DELAY":
        instr=input()
        if instr.isdigit():
            glitch_delay=int(instr)
    if cmd == "CMD_PULSE":
        instr=input()
        if instr.isdigit():
            glitch_pulse=int(instr)
    if cmd=="START":
        glitch_thread(1,glitch_delay,glitch_pulse)
    if cmd == "STOP":
        print("stop")
        power33.value(0)
        

