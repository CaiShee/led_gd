import os
import torch
import time
import torch.utils.data as Data
import numpy as np
from _01NetBase import BP, ResNet
from torch import nn

'''
数据集和训练设备及模型的基本信息
'''
feature_normal = 3000
label_normal = 4
data_path = os.path.join("DataBase", "_data_1_.csv")
model_path = os.path.join("models", "final_02.pt")
device = torch.device("cpu")
feature_num = 9
label_num = 3


def GetData(data_path, feature_num, label_num):
    data = np.genfromtxt(data_path, delimiter=',', dtype=float)
    data = torch.Tensor(data)
    features = data[:, :feature_num]
    labels = data[:, feature_num:feature_num+label_num]
    return features, labels


if __name__ == "__main__":

    # %% 准备阶段
    batchsize = 512
    epcho = 1500
    lr = 1e-3

    features, labels = GetData(
        data_path=data_path, feature_num=feature_num, label_num=label_num)
    normal_features = features/feature_normal
    normal_labels = labels/label_normal
    dataset = Data.TensorDataset(normal_features, normal_labels)
    train_iter = Data.DataLoader(
        dataset, batchsize, shuffle=True, num_workers=0)
    test_iter = Data.DataLoader(
        dataset, batchsize, shuffle=True, num_workers=0)

    node = [feature_num, 100, 100, 50, label_num]
    act = [nn.ReLU6(), nn.ReLU6(), nn.ReLU6(), nn.ReLU6()]
    myNet = ResNet(node, act)

    optimizer = torch.optim.Adam(params=myNet.parameters(), lr=lr)
    Loss = nn.MSELoss()

    myNet = myNet.to(device)
    Loss = Loss.to(device)

    total_train_step = 0
    total_test_step = 0
    myNet.train()
    start_time = time.time()

    logpath = os.path.join("Logs", "train", "{}.txt".format(start_time))
    file = open(logpath, 'w', encoding='utf-8')
    logcontent = ""

    # %% 训练过程开始
    for i in range(epcho):

        for data in train_iter:
            features, targets = data
            features = features.to(device)
            targets = targets.to(device)
            outputs = myNet(features)
            loss = Loss(outputs, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_train_step += 1
        total_test_loss = 0
        with torch.no_grad():
            for data in test_iter:
                features, targets = data
                features = features.to(device)
                targets = targets.to(device)
                outputs = myNet(features)
                loss = Loss(outputs, targets)
                total_test_loss += loss.item()
        src_head = "第{}轮：".format(i+1)
        src = "在测试集上的总误差:{}".format(total_test_loss)
        logcontent += (src_head+src+"\n")

        if (i+1) % 50 == 0:
            print("============第{}轮============".format(i+1))
            print(src)

    end_time = time.time()
    totaltime = "{:.3f}".format(end_time-start_time)
    log = "batchsize: {}\nepcho: {}\nlr: {}\ntotal_time: {}s\n".format(
        batchsize, epcho, lr, totaltime)
    file.write(log+logcontent)
    file.close()

    # %% 训练过程结束,保存模型
    torch.save(myNet, model_path)
