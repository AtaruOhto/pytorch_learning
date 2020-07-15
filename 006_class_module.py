# -*- coding: utf-8 -*-
"""006_class_module.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18ToVwtFqiclTy3EqLGu7fU1bknnmRUjt
"""

"""
ネットワークのモジュール化

クラスとして、ニューラルネットワークを定義する
参考: https://www.shoeisha.co.jp/book/detail/9784798157184
"""

import torch
from torch import nn

# nn.Moduleを継承したクラスを定義する
class MyLinear(nn.Module):
  def __init__(self, in_features, out_features, bias=True, p=0.5):
    super().__init__()
    self.linear = nn.Linear(
        in_features,
        out_features,
        bias
    )
    self.relu = nn.ReLU()
    self.drop = nn.Dropout(p)

  # forwardメソッドを実装することで、PyTorchの自動微分が有効になる。
  # 内部でforwardを呼び出す。 https://github.com/pytorch/pytorch/blob/v1.3.0/torch/nn/modules/module.py#L531
  def forward(self, x):
    x = self.linear(x)
    x = self.relu(x)
    x = self.drop(x)
    return x

class MyMLP(nn.Module):
  def __init__(self, in_features, out_features):
    super().__init__()
    self.ln1 = MyLinear(in_features, 200)
    self.ln2 = MyLinear(200, 200)
    self.ln3 = MyLinear(200, 200)
    self.ln4 = MyLinear(200, out_features)

  def forward(self, x):
    x = self.ln1(x)
    x = self.ln2(x)
    x = self.ln3(x)
    x = self.ln4(x)
    return x

mlp = MyMLP(64, 10)
print(mlp)





