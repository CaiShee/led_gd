from _02Threads import *
import numpy as np
import math
import cv2
from queue import Queue
import socket


class Player2D(BasicThread):
    '''
        2D播放器
    '''

    def __init__(self, data_queue: Queue):
        super().__init__()
        self.data_queue = data_queue
        pass

    def update(self):
        xyz = self.data_queue.get()
        canvas = 40*np.ones((600, 600, 3), dtype=np.uint8)
        x0 = float(xyz[0, 0])
        y0 = float(xyz[0, 1])
        z0 = float(xyz[0, 2])
        r = 5
        x = int(50*x0+100)
        y = int(-50*y0+500)

        cv2.circle(canvas, (int(x), int(y)), r, (200, 80, 40), 15)
        cv2.imshow('2D', canvas)
        cv2.waitKey(10)


class PlayerUnity(BasicThread):
    '''
    Unity 播放器
    '''

    def __init__(self, data_queue: Queue):
        super().__init__()
        self.data_queue = data_queue
        self.host = '127.0.0.1'
        self.port = 5005
        self.socket = None
        pass

    def start(self):
        try:
            self.socket = self.connect_unity(self.host, self.port)
        except Exception as e:
            print(e)

    def update(self):

        xyz = self.data_queue.get()
        x0 = float(xyz[0, 0])
        y0 = float(xyz[0, 1])
        z0 = float(xyz[0, 2])
        xyz_0 = np.array([x0, y0, z0])
        try:
            self.send_to_unity(xyz_0, self.socket)
            self.rec_from_unity(self.socket)
        except:
            self.socket = self.connect_unity(self.host, self.port)
        time.sleep(0.001)

    @staticmethod
    def connect_unity(host: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock

    @staticmethod
    def send_to_unity(arr: np.ndarray, sock: socket.socket):
        arr_list = arr.flatten().tolist()
        data = '' + ','.join([str(elem) for elem in arr_list]) + ''
        sock.sendall(bytes(data, encoding="utf-8"))

    @staticmethod
    def rec_from_unity(sock: socket.socket):
        data = sock.recv(1024)
        data = str(data, encoding='utf-8')
        data = data.split(',')
        new_data = []
        for d in data:
            new_data.append(float(d))
        return new_data


if __name__ == "__main__":
    q = Queue(maxsize=1)
    play = Player2D(q)
