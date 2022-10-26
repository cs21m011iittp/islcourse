# -*- coding: utf-8 -*-
"""hubconf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f_zKNlgle9djaagVvDtJoic-TFa21GEI
"""

import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, ToPILImage
from PIL import Image
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

transform_tensor_to_pil = ToPILImage()
transform_pil_to_tensor = ToTensor()

def load_data():

    # Download training data from open datasets.
    training_data = datasets.FashionMNIST(
        root="data",
        train=True,
        download=True,
        transform=ToTensor(),
    )

    # Download test data from open datasets.
    test_data = datasets.FashionMNIST(
        root="data",
        train=False,
        download=True,
        transform=ToTensor(),
    )
    return training_data, test_data

training_data, test_data = load_data()
#mod_train_data = ModifiedDataset(training_data)
#mod_test_data = ModifiedDataset(test_data)

print (training_data[0][0].shape)
#print (mod_train_data[0][0].shape)

def create_dataloaders(training_data, test_data, batch_size=64):

    # Create data loaders.
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)

    for X, y in test_dataloader:
        print(f"Shape of X [N, C, H, W]: {X.shape}")
        print(f"Shape of y: {y.shape} {y.dtype}")
        break
        
    return train_dataloader, test_dataloader

print (len(set([y for x,y in training_data])))

train_loader, test_loader = create_dataloaders(training_data, test_data, batch_size = 32)

class cs21m011(nn.Module):
    def __init__(self):
        super().__init__()
        self.m = nn.Softmax(dim =1)
        self.fc1 = nn.Linear(28*28*1, 120)
        self.fc2 = nn.Linear(120, 10)

    def forward(self, x):
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = self.m(x)
        return x

y = (len(set([y for x,y in training_data])))
model = cs21m011()

#train the network
def train_network(train_loader, optimizer,criteria, e):
  for epoch in range(e):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(inputs)
        #print(outputs.shape, labels.shape)
        tmp = torch.nn.functional.one_hot(labels, num_classes= 10)
        loss = criteria(outputs, tmp)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
            running_loss = 0.0

  print('Finished Training')

def loss_fun(y_pred, y_ground):
  v = -(y_ground * torch.log(y_pred + 0.0001))
  v = torch.sum(v)
  return v

x,y = training_data[0]
model = cs21m011()
y_pred = model(x)
print(y_pred.shape)
print(y_pred)
print(torch.sum(y_pred))
#cross_entropy(10,y_pred)

y_ground = y
loss_val = loss_fun(y_pred, y_ground)
print(loss_val)

optimizer = optim.SGD(model.parameters(), lr=0.001)

train_network(train_loader,optimizer,loss_fun,10)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

from torchmetrics import F1Score,Recall,Precision,Accuracy

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            #X, y = X.to(device), y.to(device)
            tmp = torch.nn.functional.one_hot(y, num_classes= 10)
            pred = model(X)
            test_loss += loss_fn(pred, tmp).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

    accuracy = Accuracy()
    print('Accuracy: ',accuracy(pred, y))

    precision = Precision(average='macro', num_classes=10)
    print('Precision: ',precision(pred,y))

    recall = Recall(average='macro', num_classes=10)
    print('Recall: ',recall(pred,y))

    f1 = F1Score(num_classes=10)
    print('F1 Score: ',f1(pred, y))

    return [accuracy(pred, y).item(),precision(pred,y).item(),recall(pred,y).item(),f1(pred,y).item()]

test(test_loader, model, loss_fun)

def get_model(train_loader,num_epochs=2):
    model = cs21m011()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    loss_val = loss_fun(y_pred, y_ground)

    train_network(train_loader,optimizer,loss_fun,10)
    return model

def test_model(model1, test_data_loader):
    a,p,r,f1 = test(test_data_loader, model1, loss_fun)
    return a,p,r,f1

examplerollnum = 'cs21m011'

examplerepo = examplerollnum + 'iittp/islcourse:exercise1'

entrypoints = torch.hub.list(examplerepo,force_reload=True)

print (entrypoints)

train_data_loader1 = train_loader
test_data_loader1 = test_loader

model = torch.hub.load(examplerepo,'get_model',train_loader=train_data_loader1,e=5, force_reload=True)
# config1 = [(1,10,(3,3),1,'same'), (10,3,(5,5),1,'same'), (3,1,(7,7),1,'same')]
# model = torch.hub.load(examplerepo,'get_model_advanced',train_data_loader=train_data_loader1,n_epochs=10, lr=1e-4,config=config1, force_reload=True)

print (model)

#test_data_loader1 = None

#a,p,r,f1 = torch.hub.load(examplerepo,'test_model',model1=model,test_data_loader=test_data_loader1,force_reload=True)

#print (a,p,r,f1)

def test_model(model1, test_data_loader):
	a,p,r,f1 = test(test_data_loader, model1, loss_fun)
	return a,p,r,f1

test_data_loader1 = test_loader

a,p,r,f1 = torch.hub.load(examplerepo,'test_model',model1=model,test_data_loader=test_data_loader1,force_reload=True)

print (a,p,r,f1)

