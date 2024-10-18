############################################
# dts33a_test.py
# rev 1 - shabaz - october 2024
############################################

import serial
import sys
import time

portname = 'COM5'

# protocol details
start_byte = [0xfd]
cmd_status_query = [0x21]
cmd_utf8 = [0x01, 0x04]
cmd_stop = [0x02]
cmd_pause = [0x03]
cmd_continue = [0x04]
resp_ready = 0x4f
resp_busy = 0x4e
resp_init_complete = 0x4a
resp_ok = 0x41

# serial port setup
ser = serial.Serial()
ser.port = portname
ser.baudrate = 115200
ser.timeout = 0.1

# functions
def serial_open():
    try:
        ser.open()
    except:
        print(f"Error opening serial port {port}")
        sys.exit()

def serial_close():
    ser.close()

def dts33a_wait_for_ready():
    serial_open()
    start_time = time.time()
    while (time.time() - start_time) < 5:
        ser.write(start_byte)
        ser.write([0x00, len(cmd_status_query)])
        ser.write(cmd_status_query)
        response = ser.read(1)
        if response == b'':
            # print("No response from DTS33A")
            pass
        else:
            if response[0] == resp_ready:
                # print("DTS33A is ready")
                break
            else:
                # print("DTS33A is busy")
                time.sleep(0.1)
    serial_close()

def dts33a_speak(text, vol = -1, speed = -1, pitch = -1):
    tosend = ""
    if vol != -1:
        tosend += f"[v{vol}]"
    if speed != -1:
        tosend += f"[s{speed}]"
    if pitch != -1:
        tosend += f"[t{pitch}]"
    tosend += text

    if len(tosend) > (0xff - 2):
        print("Text too long")
        return

    dts33a_wait_for_ready()
    print(f"Sending text: {tosend}")
    serial_open()
    ser.write(start_byte)
    ser.write([0x00, len(cmd_utf8) + len(tosend)])
    ser.write(cmd_utf8)
    ser.write(tosend.encode('utf-8'))
    # read response
    response = ser.read(1)
    if response == b'':
        print("No response from DTS33A")
        serial_close()
        sys.exit()
    if response[0] == resp_ok:
        print("DTS33A accepted text")
    else:
        print(f"DTS33A did not accept text, response: {response[0]}")
    serial_close()


def maincode():
    dts33a_speak("Daisy Daisy", vol = 1, speed=0, pitch=5)
    dts33a_speak("Give me your answer do", vol = 1, speed=2, pitch=5)
    dts33a_speak("I am half crazy", vol = 1, speed=0, pitch=3)
    dts33a_speak("All for the love of you", vol = 1, speed=0, pitch=1)
    dts33a_wait_for_ready()
    print("Done")

maincode()




