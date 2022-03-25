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

vcore_list=[]
vcc18_list=[]

glitch_delay=1500
glitch_pulse=50
def adc_thread():
    global vcore_list
    global vcc18_list
    vcore_list.clear()
    vcc18_list.clear()
    power33.value(1)
    #while START_ADC:
    for i in range(1,400):
        vc=vcore.read_u16()
        v1=vcc18.read_u16()
        if vc>14000 and lock.locked():
            lock.release()
        vcore_list.append(vc)
        vcc18_list.append(v1)
    
def glitch_thread():
    global glitch_delay
    global glitch_pulse
    lock.acquire()
    utime.sleep_us(glitch_delay)
    vglitch.value(1)
    utime.sleep_us(glitch_pulse)
    vglitch.value(0)
    #times=times-1
    if lock.locked():
        lock.release()
cmd=''

while True:
    led.value(0)
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
        lock.acquire()
        _thread.start_new_thread(glitch_thread,())
        adc_thread()       
        print("start")
    if cmd == "STOP":
        print("stop")
        power33.value(0)
    if cmd == "ADC":
        for i in  range(0,len(vcore_list)):
            print(3.3*vcc18_list[i]/65535,3.3*vcore_list[i]/65535)
