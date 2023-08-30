'''
Author: caishuyang
Date: 2023-03-06 08:04:55
LastEditors: caishuyang
LastEditTime: 2023-03-08 17:51:45
Description: 发送方，接受serial数据，处理后发送给 player
'''
import datetime
from email import header
import torch
import os
from queue import Queue
from train import feature_normal, label_normal
from _02Threads import *


class Publisher(BasicThread):
    def __init__(self, q1: Queue, *q2: Queue, needLog: bool = False, feature_num=9,
                 label_num=3, modelpath="models\\final_01.pt"):
        super().__init__()
        self.rec_queue = q1
        self.pub_queue = q2
        self.feature_num = feature_num
        self.label_num = label_num
        self.model = torch.load(modelpath)
        self.model = self.model.to("cpu")

        self.needLog = needLog
        self.startTime = None
        self.file_rec = None
        self.logcontent = ""
        self.reccontent = ''

    def start(self):
        if self.needLog:
            self.startTime = time.time()
            try:
                self.file_xyz = open(os.path.join("Logs", "position", "xyz_{}.txt".format(
                    self.startTime)), 'w', encoding='utf-8')
                self.file_rec = open(os.path.join("Logs", "position", "rec_{}.txt".format(
                    self.startTime)), 'w', encoding='utf-8')
            except:
                os.makedirs(os.path.join("Logs", "position"))

                self.file_xyz = open(os.path.join("Logs", "position", "xyz_{}.txt".format(
                    self.startTime)), 'w', encoding='utf-8')
                self.file_rec = open(os.path.join("Logs", "position", "rec_{}.txt".format(
                    self.startTime)), 'w', encoding='utf-8')
            self.logcontent = ""
            self.reccontent = ''

    def update(self):
        self.pub()

    def pub(self):
        data = self.rec_queue.get()
        output = self.model(data/feature_normal)*label_normal
        time.sleep(0.001)
        for pub_queue in self.pub_queue:
            if pub_queue.full():
                pub_queue.get()
            pub_queue.put(output)

        if self.needLog:

            NowTime = round(time.time()-self.startTime, 3)
            recData = ''
            outData = ''
            header = "{} s: ".format(NowTime)
            for i in range(self.feature_num):
                recData += ('{:.3f} , '.format(float(data[0, i])))
            for i in range(self.label_num):
                outData += ('{:.3f} , '.format(float(output[0, i])))

            self.logcontent += header+'xyz : '+outData+'\n'
            self.reccontent += header+'rec : '+recData+'\n'
            print(header+'xyz : '+outData)

    def end(self):
        if self.needLog:
            self.file_xyz.write(self.logcontent)
            self.file_rec.write(self.reccontent)
            self.file_xyz.close()
            self.file_rec.close()
        print("前面的区域以后再来探索吧")


if __name__ == "__main__":
    q1 = Queue(maxsize=1)
    q2 = Queue(maxsize=1)
    publish = Publisher(q1, q2, needLog=False)
    pass
