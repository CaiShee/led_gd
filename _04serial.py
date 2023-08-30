import serial
import time
import torch
from queue import Queue
import serial.tools.list_ports
from _02Threads import *
import numpy as np


class mySerial(BasicThread):
    def __init__(self,q:Queue,real:bool,feature_num:int=9,port:str="com3", baudrate:int=115200, 
                timeout:float=0.5,data_file_path:str = "D:\\MyPrograms\\python_01\\led_gd_final\\DataBase\\data_2.csv"):
        super().__init__()
        self.queue = q
        self.real = real
        self.num = feature_num
        # 真实串口设置
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        if self.real:
            comList = list(serial.tools.list_ports.comports())
            self.port=list(comList[0])[0]

        # 虚拟串口设置
        self.data_path = data_file_path
        self.data = None
        self.len = 0
        self.pin = 0

        print(self.port)

    def awake(self):
        if self.real:
            self.open_real_ser()
        else:
            self.open_virtual_ser()

    def update(self):
        if self.real:
            self.read_real_msg()
        else:
            self.read_virtual_msg()
    
    def end(self):
        if self.real:
            self.close_real_ser()

    def open_real_ser(self):
        try:
            self.ser = serial.Serial(
                self.port, self.baudrate, timeout=self.timeout)
            if (self.ser.isOpen() == True):
                print("串口打开成功")
                print("原神，启动！")
        except Exception as exc:
            self.flag = False
            print("串口打开异常", exc)

    def open_virtual_ser(self):
        self.data = np.genfromtxt(self.data_path, delimiter=',', dtype=float)
        self.data = torch.Tensor(self.data)
        self.data = self.data[:,:self.num]
        self.len = len(self.data)
        pass

    def read_real_msg(self):
        ori_data = self.ser.read(self.ser.in_waiting).decode("utf-8")
        ori_data = ori_data.split("\t")
        time.sleep(0.001)
        if len(ori_data)>=9:
            data = list()
            for i in range(9):
                if not ori_data[i].isdigit:
                    ori_data[i] = ori_data[i].split("\n")[0]
                if ori_data[i].isdigit:
                    data.append(float(ori_data[i]))
            if len(data)==9:
                data=torch.tensor([data])
            if self.queue.full():
                self.queue.get()
            self.queue.put(data)

    def read_virtual_msg(self):
        count = int(self.pin%self.len)
        oridata = self.data[count,:]
        data = torch.Tensor.reshape(oridata,(1,self.num))
        self.pin+=1
        time.sleep(0.01)
        if self.queue.full():
            self.queue.get()
        self.queue.put(data)      
        pass

    def close_real_ser(self):
        try:
            self.ser.close()
            if self.ser.isOpen():
                print("串口未关闭")
            else:
                print("关闭串口，喵~")
        except Exception as exc:
            print("串口关闭异常", exc)




if __name__ == '__main__':
    q=Queue(maxsize=1)
    myser = mySerial(q,True)
    myser.open_real_ser()
    myser.read_real_msg()
    myser.close_real_ser()
    