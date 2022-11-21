# -*- coding: utf-8 -*-
"""hubconf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yPcwLCzBeSn3PzwVhc_lOnDvak_h-kvr
"""

"""# Part1"""
import torch
import numpy as np
import sklearn
from sklearn.datasets import make_blobs,make_circles
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import homogeneity_score
from sklearn.metrics.cluster import completeness_score
from sklearn.metrics.cluster import v_measure_score

def get_data_blobs(n_points=100):
  X, y = make_blobs(n_samples=n_points, centers=3, n_features=2,random_state=0)
  return X,y

def get_data_circles(n_points=100):
  X, y = make_circles(n_samples = n_points)
  return X,y

def get_data_mnist():
  X,y = load_digits(return_X_y=True)
  #print(X.shape)
  return X,y

def build_kmeans(X=None,k=10):
  kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
  return kmeans

def assign_kmeans(km=None,X=None):
  ypred = km.predict(X)
  return ypred

def compare_clusterings(ypred_1=None,ypred_2=None):
  h = homogeneity_score(ypred_1,ypred_2)
  c =completeness_score(ypred_1,ypred_2)
  v = v_measure_score(ypred_1,ypred_2)
  return h,c,v


"""# Part2"""
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score


def get_data_mnist():
  X,y = load_digits(return_X_y=True)
  #print(X.shape)
  return X,y

def build_lr_model(X=None, y=None):
  lr_model = LogisticRegression(random_state=0,max_iter=10000).fit(X, y)
  return lr_model

def build_rf_model(X=None, y=None):
  rf_model = RandomForestClassifier(max_depth=2, random_state=0)
  rf_model.fit(X,y)
  return rf_model

def get_metrics(model1=None,X=None,y=None):
  y_pred = model1.predict(X)
  acc = accuracy_score(y, y_pred)
  prec = precision_score(y, y_pred, average='micro')
  rec = recall_score(y, y_pred, average='micro')
  f1 = f1_score(y, y_pred, average='micro')
  auc = roc_auc_score(y, model1.predict_proba(X), multi_class='ovr')
  return acc, prec, rec, f1, auc

###part2b###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, cross_val_score

# imporitn the data set from the sklearn
from sklearn.datasets import load_digits 

#import the classifier and performance matrix

from sklearn import svm, metrics

x,y = get_data_mnist()


def get_paramgrid_lr():
  mlp_prmtr_lr = {
    'solver' : ['lbfgs'],
    'max_iter' : [100,110,120,130,140],
    'alpha' : 10.0 ** -np.arange(1,10),
    'hidden_layer_sizes' : np.arange(10,15),
    'random_state' : [0,1,2,3,4]   
  }
  return mlp_prmtr_lr

def get_paramgrid_rf():
  mlp_prmtr_rf = {
    'solver' : ['lbfgs'],
    'max_iter' : [100,110,120,130,140],
    'alpha' : 10.0 ** -np.arange(1,10),
    'hidden_layer_sizes' : np.arange(10,15),
    'random_state' : [0,1,2,3,4]   
  }
  return mlp_prmtr_rf
  
def perform_gridsearch_cv_multimetric(model1=None, param_grid=None, cv=5, X=Xtrain, y=ytrain, metrics=['accuracy','roc_auc']):
    #GSCV for logistic regression
    grid = GridSearchCV(SVC(), lt_dict=get_paramgrid_lr(), refit = True, verbose = 3)
    grid.fit(X, y)
    #print(grid.best_params_)

    #GSCV for random forest
    rndm_model_grid = RandomForestClassifier(random_state=42)
    rndm_model_gridCV = GridSearchCV(estimator = rndm_model_grid,rf_dict=get_paramgrid_rf(), cv = 5)
    rndm_model_gridCV.fit(X,y)

    #print(rndm_model_gridCV.best_params_)

    test_scores=[]
    test_scores.append(grid.best_params_)
    test_scores.append(rndm_model_gridCV.best_params_)

    return test_scores


"""# Part3"""
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, ToPILImage
from PIL import Image
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


def load_data():
    train_data = datasets.MNIST(
        root="data",
        train=True,
        download=True,
        transform=ToTensor(), 
    )

  # Download test data from open datasets.
    test_data = datasets.MNIST(
        root="data",
        train=False,
        download=True,
        transform=ToTensor(),
    )

    return train_data, test_data

def get_mnist_tensor():
    X, y = load_data()
    return X,y

train_data, test_data=get_mnist_tensor()

for X, y in train_data:
        print(f"Shape of X [N, C, H, W]: {X.shape}")
        #print(f"Shape of y: {y.shape} {y.dtype}")
        break

def cross_entropy(y_pred,y):
    v=-(y*torch.log(y_pred+0.0001))
    v=torch.sum(v)
    return v

class MyNN(nn.Module):
    def __init__(self,inp_dim=64,hid_dim=13,num_classes=10):
        super(MyNN,self).__init__()

        self.fc_encoder = nn.Conv2d(in_channels=1,out_channels=hid_dim,kernel_size=6,stride=1,padding=0)  # write your code inp_dim to hid_dim mapper

        self.fc_decoder = nn.ConvTranspose2d(in_channels=hid_dim,out_channels=inp_dim,kernel_size=6,stride=1,padding=0)  # write your code hid_dim to inp_dim mapper

        self.fc_classifier = nn.Linear(inp_dim,num_classes) # write your code to map hid_dim to num_classes
        
        self.relu=nn.ReLU()

        self.softmax = nn.Softmax(dim=1)


    def forward(self,x):
        x = torch.flatten(x) # write your code - flatten x
        x_enc = self.fc_encoder(x)
        print(x_enc.shape)
        x_enc = self.relu(x_enc)
        
        y_pred = self.fc_classifier(x_enc)
        y_pred = self.softmax(y_pred)
        
        x_dec = self.fc_decoder(x_enc)
      
        return y_pred, x_dec
  
    # This a multi component loss function - lc1 for class prediction loss and lc2 for auto-encoding loss
    def loss_fn(self,x,yground,y_pred,xencdec):
        # class prediction loss
        # yground needs to be one hot encoded - write your code
        lc1 = cross_entropy(y_pred,yground) # write your code for cross entropy between yground and y_pred, advised to use torch.mean()
        
        # auto encoding loss
        lc2 = torch.mean((x - xencdec)**2)
        
        lval = lc1 + lc2
    
        return lval

  
    # This a multi component loss function - lc1 for class prediction loss and lc2 for auto-encoding loss
    def loss_fn(self,x,yground,y_pred,xencdec):
        # class prediction loss
        # yground needs to be one hot encoded - write your code
        lc1 = cross_entropy(y_pred,yground) # write your code for cross entropy between yground and y_pred, advised to use torch.mean()
        
        # auto encoding loss
        lc2 = torch.mean((x - xencdec)**2)
        
        lval = lc1 + lc2
    
        return lval

def get_mynn(inp_dim=64,hid_dim=13,num_classes=10):
    mynn = MyNN(inp_dim,hid_dim,num_classes)
    return mynn

device='cuda' if torch.cuda.is_available() else 'cpu'
device

mynn=get_mynn().to(device)

def get_loss_on_single_point(mynn,x0,y0):
    y_pred, xencdec = mynn(x0)
    lossval = mynn.loss_fn(x0,y0,y_pred,xencdec)
    # the lossval should have grad_fn attribute set
    return lossval

x0=train_data[0][0]
x0=x0.to(device)

y0=train_data[0][1]

l=get_loss_on_single_point(mynn,x0,x0)

def train_combined_encdec_predictor(mynn,X,y, epochs=11):
  # X, y are provided as tensor
  # perform training on the entire data set (no batches etc.)
  # for each epoch, update weights
  
  optimizer = optim.SGD(mynn.parameters(), lr=0.01)
  
  for i in range(epochs):
    optimizer.zero_grad()
    ypred, Xencdec = mynn(X)
    lval = mynn.loss_fn(X,y,ypred,Xencdec)
    lval.backward()
    optimizer.step()
    
  return mynn
