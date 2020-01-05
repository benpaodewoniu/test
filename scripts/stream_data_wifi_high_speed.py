from __future__ import print_function
import sys

sys.path.append('..')  # help python find cyton.py relative to scripts folder
from threading import Thread
from openbci import wifi as bci
import logging
import matplotlib.pyplot as plt
import numpy as np

EEG_LENGTH = 100
arr = []


def getData(sample):
    # print(sample)
    arr.append(sample.channel_data[0])
    print(sample.channel_data[0])


def proc2():
    figure2 = plt.figure()
    fig1 = figure2.add_subplot(1, 2, 1)
    fig2 = figure2.add_subplot(1, 2, 2)
    data = []
    i = 0
    x = np.linspace(0, 2, EEG_LENGTH)
    while True:
        print(len(arr))
        if len(arr) > 0:
            data.append(arr.pop())
        if len(data) == EEG_LENGTH:
            fig2.cla()
            fig2.plot(x, data)
            data = data[1:]
            plt.xticks([])
            plt.yticks([])
            plt.pause(0.001)
            fig1.cla()


if __name__ == '__main__':
    logging.basicConfig(filename="test.log", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('---------LOG START-------------')
    # If you don't know your IP Address, you can use shield name option
    # If you know IP, such as with wifi direct 192.168.4.1, then use ip_address='192.168.4.1'
    shield_name = 'OpenBCI-3F2F'
    shield = bci.OpenBCIWiFi(shield_name=shield_name, log=True, high_speed=True)
    print(1)
    print(shield)
    print(2)
    print("WiFi Shield Instantiated")
    p = Thread(target=proc2)
    # p.start()
    print(444)
    shield.start_streaming(getData)
    shield.loop()
