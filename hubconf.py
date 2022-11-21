# -*- coding: utf-8 -*-
"""hubconf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yPcwLCzBeSn3PzwVhc_lOnDvak_h-kvr
"""

import torch
import numpy as np
import sklearn
from sklearn.datasets import make_blobs,make_circles
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

###part1###
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
