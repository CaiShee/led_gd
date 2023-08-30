from email.header import Header
import os
import glob
import numpy as np
import pandas as pd

global Dark, LastTime, Thresh, X_num

Dark = 3500
LastTime = 30
Thresh = 50
X_num = 8


def dealMatlist(matX: tuple):
    mat = matX[0]
    x = matX[1]
    matlist = list()
    aver = np.mean(mat)
    for line in mat:
        if abs(np.mean(line) - aver) < Thresh:
            matlist.append(line)
    mat = np.array(matlist)
    try:
        result1 = np.concatenate((mat, x*np.ones((len(mat), 1))), axis=1)
    except:
        print(x)
        raise ("error")
    result2 = np.mean(result1, axis=0)
    return result1, np.reshape(result2, (1, len(result2)))


def dealTxt(txt_path: str):
    oriData = np.loadtxt(txt_path)
    matsList = list()
    matlist = list()
    flag = True
    for line in oriData:
        if np.mean(line) > Dark:
            if (len(matlist) > LastTime) & flag:
                matlist = matlist[int(0.15*len(matlist)):int(0.85*len(matlist))]
                matsList.append((np.array(matlist), len(matsList)+1))
            matlist.clear()
            flag = False
        else:
            flag = True
            matlist.append(line)
        if len(matsList) == X_num:
            break

    oriresult = list(map(dealMatlist, matsList))
    start_1, start_2 = oriresult[0]
    for i in range(1, len(oriresult)):
        start_1 = np.concatenate((start_1, oriresult[i][0]), axis=0)
        start_2 = np.concatenate((start_2, oriresult[i][1]), axis=0)

    return start_1, start_2


def dealDataFile(data_path: str = os.path.join('DataBase', 'Data')):
    z_files = glob.glob(os.path.join(data_path, '*'))
    results_1 = list()
    results_2 = list()
    for z_file in z_files:
        z = float(os.path.basename(z_file))
        y_files = glob.glob(os.path.join(z_file, '*'))

        for y_file in y_files:
            y = float(os.path.basename(y_file).split('.')[0])
            try:
                result_1, result_2 = dealTxt(y_file)
            except:
                print('在'+str(z)+':'+str(y)+'.txt')
            result_1 = np.concatenate(
                (result_1, y*np.ones((len(result_1), 1))), axis=1)
            result_1 = np.concatenate(
                (result_1, z*np.ones((len(result_1), 1))), axis=1)
            result_2 = np.concatenate(
                (result_2, y*np.ones((len(result_2), 1))), axis=1)
            result_2 = np.concatenate(
                (result_2, z*np.ones((len(result_2), 1))), axis=1)
            results_1.append(result_1)
            results_2.append(result_2)

    start_1 = results_1[0]
    for i in range(1, len(results_1)):
        start_1 = np.concatenate((start_1, results_1[i]), axis=0)
    results_2 = np.array(results_2)
    results_2 = np.reshape(
        results_2, (results_2.shape[0]*results_2.shape[1], results_2.shape[2]))
    return start_1, results_2


if __name__ == "__main__":
    result_1, result_2 = dealDataFile(os.path.join('DataBase', 'Data_v2'))
    np.savetxt(os.path.join("DataBase", "_data_1_.csv"),
               result_1, delimiter=",")
    np.savetxt(os.path.join("DataBase", "_data_2_.csv"),
               result_2, delimiter=",")
