import sys
import time

import cv2
import serial
import win32gui
from PIL import ImageGrab
from PyQt5 import QtWidgets
from numpy import *

import design
from port import serial_ports, speeds

WINDOW_SUBSTRING = "Asterios"
global hwhw

def get_window_info():
    window_info = {}
    win32gui.EnumWindows(set_window_coordinates, window_info)
    return window_info


def set_window_coordinates(hwnd, window_info):
    global hwhw
    if win32gui.IsWindowVisible(hwnd):
        if WINDOW_SUBSTRING in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            window_info['x'] = x
            window_info['y'] = y
            window_info['width'] = w
            window_info['height'] = h
            window_info['name'] = win32gui.GetWindowText(hwnd)
            hwhw = hwnd
            win32gui.SetForegroundWindow(hwnd)


class Fisher(QtWidgets.QMainWindow, design.Ui_Fisher_0_0_1):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port.addItems(serial_ports())
        self.speed.addItems(speeds)
        self.realport = None
        self.connect_Button.clicked.connect(self.connect)
        self.start_Button.clicked.connect(self.start)
        self.stop_Button.clicked.connect(self.stop)
        self.window_info = get_window_info()
        self.box = (self.window_info['x'] + 8, self.window_info['y'] + 31, int(self.window_info['width'] + self.window_info['x']) - 8,int( self.window_info['height'] + self.window_info['y']) - 8)
        self.__calc_count2 = None
        self.perem1 = None
        self.perem2 = None
        self.__minimal = None



    def connect(self):
        try:
            self.realport = serial.Serial(self.port.currentText(), int(self.speed.currentText()))
            self.connect_Button.setStyleSheet("background-color: green")
            self.connect_Button.setText('Подключено')
        except Exception as e:
            print(e)

    def get_screen(self):
        screen = ImageGrab.grab(self.box)
        screen.save("screen2.bmp", "BMP")


    def gogowork(self):
        global hwhw
        win32gui.SetForegroundWindow(hwhw)
        self.get_screen()

    @property
    def calculat(self):
        low_red = (189, 131, 0)
        high_red = (228, 160, 0)
        self.__calc_count2 = cv2.countNonZero(cv2.inRange(cv2.imread('screen2.bmp'), low_red, high_red))
        return self.__calc_count2



    def start(self):
        print('закидываем удочку')
        self.realport.write(b'e')
        self.gogowork()
        self.perem1 = self.calculat
        self.__minimal = self.perem1
        cnt = 0
        while 1:
            time.sleep(0.8)
            self.gogowork()
            self.perem2 = self.calculat
            print(self.perem1, ' ---> ',self.perem2)
            if self.perem1 == self.perem2:
                if self.perem1 != self.__minimal:
                    print('пампинг')
                    self.realport.write(b'd')
                    cnt = 20
                    #self.perem1 = self.perem2
                else:
                    cnt += 1
            else:
                if self.perem2 > self.perem1:
                    if self.perem1 != self.__minimal:
                        print('рэлинг')
                        self.realport.write(b'b')
                        cnt = 20
                        #self.perem1 = self.perem2
            self.perem1 = self.perem2
            if cnt == 30:
                print('закидываем удочку')
                self.realport.write(b'e')
                self.gogowork()
                self.perem1 = self.calculat
                self.__minimal = self.perem1
                cnt = 0





    def send1(self):
        if self.realport:
            self.realport.write(b'd')

    def send2(self):
        if self.realport:
            self.realport.write(b'b')

    def stop(self):
        if self.realport:
            self.realport.close()
            self.connect_Button.setStyleSheet("background-color: red")
            self.connect_Button.setText('Выключено')


def main():

    app = QtWidgets.QApplication(sys.argv)
    window = \
        Fisher()
    window.show()
    app.exec_()



if __name__ == '__main__':
    main()
