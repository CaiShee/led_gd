import os
import torch
import numpy as np
from train import GetData, feature_normal, label_normal, data_path, model_path, device

if __name__ == "__main__":
    myNet = torch.load(os.path.join("models", "final_01.pt"))
    myNet.to("cpu")
    myNet.eval()
    features, labels = GetData(data_path=os.path.join(
        "DataBase", "data_2_.csv"), feature_num=9, label_num=3)
    normal_features = features/feature_normal
    normal_labels = labels/label_normal
    lossmat = torch.Tensor.abs(myNet(normal_features)*label_normal-labels)
    eval_data = (myNet(normal_features)*label_normal).detach().numpy()
    np.savetxt(os.path.join("DataBase", "eval_2_.csv"),
               eval_data, delimiter=",")
    print(torch.Tensor.mean(lossmat))
