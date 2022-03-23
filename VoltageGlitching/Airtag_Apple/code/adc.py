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

vcore_list=[]
vcc18_list=[]
def adc_thread(times):

    global vcore_list
    global vcc18_list
    vcore_list.clear()
    vcc18_list.clear()
    #while START_ADC:
    for i in range(1,times):
        vc=vcore.read_u16()
        v1=vcc18.read_u16()
        vcore_list.append(vc)
        vcc18_list.append(v1)

cmd=''

while True:
    cmd=input()
    if cmd=="START":
        power33.value(1)
        adc_thread(500)
        print(len(vcore_list),len(vcc18_list))

    if cmd == "STOP":
        START_ADC = False
        power33.value(0)
        print("stop")
        #lock.release()
    if cmd == "ADC":
        for i in  range(0,len(vcore_list)):
            print(3.3*vcc18_list[i]/65535,3.3*vcore_list[i]/65535)

