
from keyboard import *
from _02Threads import *
from _04serial import *
from _03Player import *
from _05Publisher import *
from queue import Queue


if __name__ == "__main__":

    q1 = Queue(maxsize=1)
    q2 = Queue(maxsize=1)
    q3 = Queue(maxsize=1)
    ser = mySerial(q=q1, real=False)
    pub = Publisher(q1, q2, q3, needLog=True,
                    modelpath="D:\\MyPrograms\\python_01\\led_gd_final\\models\\final_01.pt")
    player_1 = Player2D(q2)
    player_2 = PlayerUnity(q3)

    add_hotkey('q', quit, args=(player_1, pub, ser))
    pool = ThreadsPool(ser, pub, player_1)
    pool.EXecute()

    pass
