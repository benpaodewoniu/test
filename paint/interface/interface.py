import time
import os
import sys
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt

pwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.dirname(pwd) + os.path.sep + "."))

b = False

class Interface:

    def __init__(self):
        self.figure = plt.figure(1)
        self.logo_path = './image/logo.gif'

    def rmAxis(self):
        frame = plt.gca()
        frame.axes.get_yaxis().set_visible(False)
        frame.axes.get_xaxis().set_visible(False)
        plt.axis('off')

    def showMain(self):
        self.figure.clf()
        fig1 = self.figure.add_subplot(2, 1, 1)
        self.rmAxis()
        fig2 = self.figure.add_subplot(2, 1, 2)
        self.rmAxis()
        plt.ion()
        img = plt.imread(self.logo_path)
        fig1.imshow(img)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        fig2.text(0.5, 0.5, u"智能感知中心脑电系统V1", fontsize=15, horizontalalignment="center",
                  bbox=dict(boxstyle='round,pad=0.5', fc='blue', ec='k', lw=1, alpha=0.5))
        plt.pause(3)

    def ready(self):
        self.figure.clf()
        fig = self.figure.add_subplot(1, 1, 1)
        self.rmAxis()
        prompt = "即将开始测试硬件连接"
        while True:
            for i in range(len(prompt)):
                fig.cla()
                t_prompt = prompt[0:i]
                fig.text(0.5, 0.5, t_prompt, fontsize=15, horizontalalignment="center",
                         bbox=dict(boxstyle='round,pad=0.5', fc='blue', ec='k', lw=1, alpha=0.5))
                plt.pause(0.2)
            break
        plt.close(self.figure)
