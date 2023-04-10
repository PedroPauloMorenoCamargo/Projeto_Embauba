import pyautogui
import serial
import argparse
import time
import logging
import os
import subprocess
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class MyControllerMap:
    def __init__(self):
        self.button = {'espaco': 'space', 'control':'ctrl','direita':'right','esquerda':'left','shift':'shift','aumenta':'up','diminui': 'down','Shuffle':'s','Refresh':'r'} # Fast forward (10 seg) pro Youtube # Fast forward (10 seg) pro Youtube

class SerialControllerInterface:
    # Protocolo
    # byte 1 -> Botão 1 (estado - Apertado 1 ou não 0)
    # byte 2 -> EOP - End of Packet -> valor reservado 'X'

    def __init__(self, port, baudrate):
        self.ser = serial.Serial('COM3', baudrate=baudrate)
        self.mapping = MyControllerMap()
        self.incoming = '0'
        pyautogui.PAUSE = 0  ## remove delay
    
    def update(self):
        ## Sync protocol
        print("update")   
        while self.incoming != b'X':
            self.incoming = self.ser.read()
            logging.debug("Received INCOMING: {}".format(self.incoming))
            print("lendo")

        data = self.ser.read()
        logging.debug("Received DATA: {}".format(data))

        if data == b'p':
            print("Play")
            pyautogui.keyDown(self.mapping.button['espaco'])
            pyautogui.keyUp(self.mapping.button['espaco'])
            self.ser.write('P'.encode(encoding = 'ascii', errors = 'strict'))
        elif data == b'f':
            print("Forward")
            pyautogui.hotkey(self.mapping.button['control'],self.mapping.button['direita'])
            self.ser.write('F'.encode(encoding = 'ascii', errors = 'strict'))
        elif data == b'v':
            print("Backward")
            pyautogui.hotkey(self.mapping.button['control'],self.mapping.button['esquerda'])
            self.ser.write('B'.encode(encoding = 'ascii', errors = 'strict'))
        elif data == b's':
            print("Shuffle")
            pyautogui.hotkey(self.mapping.button['control'],self.mapping.button['Shuffle'])
            self.ser.write('S'.encode(encoding = 'ascii', errors = 'strict'))
        elif data == b'r':
            print("Refresh")
            pyautogui.hotkey(self.mapping.button['control'],self.mapping.button['Refresh'])
            self.ser.write('R'.encode(encoding = 'ascii', errors = 'strict'))
        else:
            print("Volume")  
            volume_novo = int.from_bytes(data , "big")-98
            volume.SetMasterVolumeLevel(volume_novo, None)
            self.ser.write('V'.encode(encoding = 'ascii', errors = 'strict'))

       
        self.incoming = self.ser.read()      
 

class DummyControllerInterface:
    def __init__(self):
        self.mapping = MyControllerMap()

    def update(self):
        pyautogui.keyDown(self.mapping.button['A'])
        time.sleep(0.1)
        pyautogui.keyUp(self.mapping.button['A'])
        logging.info("[Dummy] Pressed A button")
        time.sleep(1)


if __name__ == '__main__':
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    interfaces = ['dummy', 'serial']
    controller = SerialControllerInterface(port="COM3", baudrate=115200)
    '''n_teve_handshake= True
    while n_teve_handshake:
        n_teve_handshake = controller.handshake()'''
    while True:
        controller.update()
        
    