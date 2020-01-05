from __future__ import print_function
import time
import sys
from multiprocessing import Queue

sys.path.append('..')
from openbci import wifi as bci
import numpy as np
from paint.interface.interface import Interface
from collections import deque
import matplotlib.pyplot as plt
from multiprocessing import Process

q = Queue()
_q = Queue()
cq = Queue()
c_q = Queue()


def printData(sample):
    if q.qsize() < 2:
        d = sample.channel_data[0]
        q.put(d)
        _q.put(d)
    if _q.qsize() < 2:
        d = sample.channel_data[1]
        _q.put(d)
        c_q.put(d)
    print(sample.channel_data[0])


def proc2(q, _q):
    data1 = []
    data2 = []
    fig = plt.figure(figsize=(20, 10))
    fig1 = fig.add_subplot(1, 2, 1)
    fig2 = fig.add_subplot(1, 2, 2)
    fig3 = fig.add_subplot(2, 1, 1)
    while True:
        data1.append(q.get())
        data2.append(_q.get())
        if len(data1) > 200:
            x = np.linspace(0, 2, len(data1))
            x1 = np.linspace(0, 2, len(data2))
            fig1.cla()
            fig2.cla()
            fig1.plot(x, data1)
            fig2.plot(x1, data2)
            data1 = data1[1:]
            data2 = data2[1:]
            plt.pause(0.00000001)
            fig1.cla()
            fig2.cla()


def classifyFinger(cq, c_q):
    pass


if __name__ == '__main__':
    # inter = Interface()
    # inter.showMain()
    # inter.ready()
    t = Process(target=proc2, args=(q, _q))
    t.start()
    c = Process(target=classifyFinger, args=(cq, c_q))
    c.start()
    shield_name = 'OpenBCI-3F2F'
    shield = bci.OpenBCIWiFi(shield_name=shield_name, log=False, high_speed=False)
    print("WiFi Shield Instantiated")
    shield.start_streaming(printData)
    shield.loop()
