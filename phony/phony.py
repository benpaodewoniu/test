from __future__ import print_function
import time
import numpy as np
import sys
import os
from random import shuffle
from multiprocessing import Queue
from PIL import Image

sys.path.append('..')
import numpy as np
import glob
import matplotlib.pyplot as plt
from multiprocessing import Process
from threading import Thread

can_classify = False

q = Queue()
_q = Queue()
result = Queue()

CLASSIFY_EEG_LEN = 20
START_EEG_LEN = 50

TYPE = ['cat', 'dog']

EEG_LIST = Queue()

def get_file_path():
    image_type = TYPE
    dir_path = os.path.join(os.path.abspath('..'), 'paint', 'image')
    image_list = []
    for type in image_type:
        dir_image_path = os.path.join(dir_path, type, '*.jpg')
        image_files = glob.glob(dir_image_path)
        shuffle(image_files)
        for image in image_files:
            image_list.append(type + '|' + image)
    return image_list


def providData(getdata):
    while True:
        time.sleep(0.1)
        d = np.random.rand()
        print(d)
        getdata(d)


def getdata(d):
    q.put(d)
    _q.put(d)


def proc2(image_list, q, _q):
    is_peace = True

    data1 = []
    data2 = []
    peace = []
    plt.ion()
    fig = plt.figure(figsize=(10, 10))
    fig1 = fig.add_subplot(2, 2, 4)
    fig2 = fig.add_subplot(2, 2, 3)
    fig3 = fig.add_subplot(2, 1, 1)

    img_index = 0
    eeg_index = 0
    while True:
        data1.append(q.get())
        data2.append(_q.get())
        if len(data1) > START_EEG_LEN:
            x = np.linspace(0, 1, len(data1))
            x1 = np.linspace(0, 1, len(data2))
            fig1.cla()
            fig2.cla()
            fig1.plot(x, data1)
            fig2.plot(x1, data2)
            s = u'close your eye and keep peace '
            if is_peace:
                fig3.text(0.5, 0.5, s, fontsize=15, horizontalalignment="center")

            # 采集到平静下的脑电波之后正式开始测试
            if eeg_index > CLASSIFY_EEG_LEN and img_index < len(image_list):
                is_peace = False
                t1 = Process(target=classify, args=(data1, data2))
                t1.start()
                img = Image.open(image_list[img_index].split('|')[1])
                fig3.imshow(img)
                img_index += 1
                eeg_index = 0
            elif img_index == len(image_list):
                fig.clf()
                s = u'data is being processed, please wait '
                for i in range(len(s)):
                    fig.clf()
                    t_prompt = s[0:i]
                    fig.text(0.5, 0.5, t_prompt, fontsize=15, horizontalalignment="center")
                    plt.pause(0.2)
                plt.pause(5)
                fig.clf()
                s = u'the dog is 70% and the cat is 30% '
                for i in range(len(s)):
                    fig.clf()
                    t_prompt = s[0:i]
                    fig.text(0.5, 0.5, t_prompt, fontsize=15, horizontalalignment="center")
                    plt.pause(0.2)
                plt.pause(10)
                return
            data1 = data1[1:]
            data2 = data2[1:]
            plt.pause(0.00000001)
            eeg_index += 1


def classify(EEG_LIST):
    while True:
        time.sleep(3)
        if len(EEG_LIST) > 0:
            pass
        print(99999)



if __name__ == '__main__':
    image_list = get_file_path()
    t = Thread(target=classify, args=(EEG_LIST,))
    t.start()
    t = Process(target=proc2, args=(image_list, q, _q))
    t.start()
    providData(getdata)
