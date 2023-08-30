import torch
from torch import nn
import torch.nn.functional as F

class BP(nn.Module):
    '''
        BP神经网络框架
    '''
    def __init__(self,node,act):
        super().__init__()
        self.node=node
        self.n=len(node)
        self.act=act 
        self.model=nn.Sequential()
        for i in range(self.n-1):
            self.model.append(nn.Linear(self.node[i],self.node[i+1]))
            self.model.append(self.act[i])

    def forward(self,input):
        output=self.model(input)
        return output

class ResNet(nn.Module):
    '''
        残差网络框架
    '''
    def __init__(self,node,act):
        super().__init__()
        self.node=node 
        self.n=len(node) 
        self.act=act 
        self.model=nn.Sequential()
        for i in range(self.n-2):
            self.model.append(nn.Linear(self.node[i],self.node[i+1]))
            self.model.append(self.act[i])
            self.model.append(ResBlock(node[i+1])) #加入残差块
        self.model.append(nn.Linear(self.node[self.n-2],self.node[self.n-1]))
        
    def forward(self,input):
        output=self.model(input)
        return output

class ResBlock(nn.Module):
    '''
        残差块
    '''
    def __init__(self,node):
        super(ResBlock,self).__init__()
        self.node=node
        self.linear1=nn.Linear(self.node,self.node)
        self.linear2=nn.Linear(self.node,self.node)
    
    def forward(self,x):
        y=F.relu(self.linear1(x))
        y=self.linear2(y)
        return F.relu(x+y)
        
if __name__=='__main__':
    bp=ResNet(node=[2,4,3],act=[nn.ReLU(),nn.Sigmoid(),nn.ReLU()])
    traindata=torch.randint(0,2,size=(4,2),dtype=torch.float32)
    labeldata=torch.randint(0,2,size=(4,3),dtype=torch.float32)
    optimizer=torch.optim.Adam(params=bp.parameters(),lr=0.01)
    Loss=nn.MSELoss()
    for i in range(10):
        yp=bp(traindata)
        loss=Loss(yp,labeldata)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(loss)