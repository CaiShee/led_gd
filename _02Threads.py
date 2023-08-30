import torch
import threading
import time
from keyboard import *


class BasicThread():
    def __init__(self) -> None:
        self.flag = True
        self.name = self
        pass

    def awake(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass

    def interface(self):
        pass

    def dealwithError(self):
        pass

    def __execute__(self):

        while self.flag:
            try:
                self.update()
            except Exception as e:
                self.dealwithError()
                print(" {} 线程异常.".format(threading.current_thread().name))
                print(e)
                print("Basic name : {}".format(self.name))


class ThreadsPool():
    def __init__(self, *threads: BasicThread) -> None:
        self.threads = list(threads)
        pass

    def ExecuteAwake(self):
        thread_list = list()
        for thread in self.threads:
            awake_thread = threading.Thread(target=thread.awake)
            awake_thread.start()
            thread_list.append(awake_thread)
        for thread in thread_list:
            thread.join()
        pass

    def ExecuteStart(self):
        thread_list = list()
        for thread in self.threads:
            start_thread = threading.Thread(target=thread.start)
            start_thread.start()
            thread_list.append(start_thread)
        for thread in thread_list:
            thread.join()

        pass

    def ExecuteUpdate(self):
        thread_list = list()
        for thread in self.threads:
            update_thread = threading.Thread(target=thread.__execute__)
            update_thread.start()
            thread_list.append(update_thread)
        pass
        for thread in thread_list:
            thread.join()

    def ExecuteEnd(self):
        for thread in self.threads:
            end_thread = threading.Thread(target=thread.end)
            end_thread.start()
        pass

    def EXecute(self):
        self.ExecuteAwake()
        self.ExecuteStart()
        self.ExecuteUpdate()
        self.ExecuteEnd()

    def AddThread(self, new_thread: BasicThread):
        self.threads.append(new_thread)


def quit(*threads: BasicThread):
    threadlist = list(threads)
    for mine in threadlist:
        mine.flag = False
        time.sleep(1e-2)


class test_1(BasicThread):
    def __init__(self) -> None:
        super().__init__()

    def awake(self):
        print("哈哈哈")
        time.sleep(2)

    def update(self):
        print("你好")
        time.sleep(0.5)


class test_2(BasicThread):
    def __init__(self) -> None:
        super().__init__()

    def start(self):
        print("hhh")
        time.sleep(2)

    def update(self):
        print("hello")
        time.sleep(0.5)


if __name__ == "__main__":
    t1 = test_1()
    t2 = test_2()
    pool = ThreadsPool(t1, t2)
    pool.EXecute()
    add_hotkey('q', quit, args=(t1, t2))
    record('q')
    pass
