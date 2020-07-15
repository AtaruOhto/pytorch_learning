# -*- coding: utf-8 -*-
"""002_pytorch_wine_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xCUpZH1zgjqofvxIZaVAB91S9Sce52a1
"""

"""
PyTorch でワインの種類を分類
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from torch.autograd import Variable
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine

# sklearnからワインのデータをロードする
wine = load_wine()
X = wine.data
Y = wine.target

feature_num = X.shape[1]
classification_num = len(np.unique(Y))

# データ情報を表示
pd.DataFrame(wine.data, columns=wine.feature_names)

# 25%を検証用データとして用いる
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.25)

train_X = torch.from_numpy(train_X).float()
train_Y = torch.from_numpy(train_Y).long()
test_X = torch.from_numpy(test_X).float()
test_Y = torch.from_numpy(test_Y).long()

# 訓練データをTensorDatasetで一組にする。
train = TensorDataset(train_X, train_Y)

# ミニバッチ学習させるために、DataLoader形式に変換する。
train_loader = DataLoader(train, batch_size=15, shuffle=True)

# ニューラルネットワークの定義
class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    unit_num = 128
    self.fc1 = nn.Linear(feature_num, unit_num)
    self.fc2 = nn.Linear(unit_num, unit_num)
    self.fc3 = nn.Linear(unit_num, unit_num)
    self.fc4 = nn.Linear(unit_num, unit_num)
    self.fc5 = nn.Linear(unit_num, unit_num)
    self.fc6 = nn.Linear(unit_num, classification_num)
    
  def forward(self, x):    
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = F.relu(self.fc3(x))
    x = F.relu(self.fc4(x))
    x = F.relu(self.fc5(x))
    x = self.fc6(x)
    return F.log_softmax(x)

model = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

for epoch in range(1500):
  total_loss = 0

  for train_x, train_y in train_loader:
    train_x, train_y = Variable(train_x), Variable(train_y)
    optimizer.zero_grad()
    output = model(train_x)
    loss = criterion(output, train_y)
    loss.backward()
    optimizer.step()
    total_loss += loss.data.item()

  if(epoch + 1) % 100 == 0:
    print(f" {epoch + 1}回目の誤差: ", total_loss / epoch)

test_x, test_y = Variable(test_X), Variable(test_Y)
result = torch.max(model(test_x).data, 1)[1]


accuracy_score = sum(test_y.data.numpy() == result.numpy()) / len(test_y.data.numpy())
print("正解率: ", accuracy_score)