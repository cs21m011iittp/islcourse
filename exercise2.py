# -*- coding: utf-8 -*-
"""exercise2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ScqofqEoHRIaOnAiRBuvgLjLWK55TI7Y
"""

#!pip install torchmetrics

import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, ToPILImage
from PIL import Image
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, precision_score

"""# Loading the data"""

def load_data():
    #download the train and test datasets
    train_data=datasets.FashionMNIST(root='data',
                                     train=True,
                                     download=True,
                                     transform=ToTensor())
    
    test_data=datasets.FashionMNIST(root='data',
                                    train=False,
                                    download=True,
                                    transform=ToTensor())
    
    return train_data,test_data

train_data,test_data=load_data()

print('size of X vector: ',train_data[0][0].shape)
print('size of Y vector:',len(set([y for x,y in train_data])))

"""# Creating the dataloaders"""

def create_dataloaders(train_data,test_data,batch_size):
    train_dataloader=DataLoader(train_data,batch_size=batch_size)
    test_dataloader=DataLoader(test_data,batch_size=batch_size)

    return train_dataloader,test_dataloader

train_loader,test_loader=create_dataloaders(train_data,test_data,batch_size=32)

"""# Preparing the Model"""

class cs21m011(nn.Module):
      def __init__(self):
          super(cs21m011,self).__init__()
          self.m=nn.Softmax(dim=1)

          self.conv1=nn.Conv2d(1,6,5)
          self.maxpool=nn.MaxPool2d(2,2)
          self.conv2=nn.Conv2d(6,16,5)

          self.fc1=nn.Linear(16*4*4,100)
          self.fc2=nn.Linear(100,10)

      def forward(self,x):
          x=self.maxpool(F.relu(self.conv1(x)))
          x=self.maxpool(F.relu(self.conv2(x)))
          x=x.view(-1,16*4*4)

          x=F.relu(self.fc1(x))
          x=self.fc2(x)
          x=self.m(x)   #applying softmax to get list of probabilities
          return x

"""# Loss function"""

def criteria(y_pred,y):
    v=-(y*torch.log(y_pred+0.0001))
    v=torch.sum(v)
    return v

model=cs21m011()

x,y=train_data[0]
print('input size: ',x.shape)
output=model(x)
print('output size: ',output.shape)
#print(output)

loss=criteria(output,y)

print('loss value: ',loss)

"""# Training the Network"""

def train_network(train_loader,optimizer,criteria,num_epochs):

    n_total_steps=len(train_loader)

    for epoch in range(num_epochs):
        train_loss=0.0

        for i,data in enumerate(train_loader,0):
            inputs,labels=data

            optimizer.zero_grad()

            outputs=model(inputs)
            #print(outputs.shape,labels.shape)

            #one hot encoding
            tmp=torch.nn.functional.one_hot(labels,num_classes=10)


            #loss function
            loss=criteria(outputs,tmp)
            loss.backward()    #finding the derivative of loss function wrt to coefficients

            optimizer.step()        #calulating the gradients

            train_loss+=loss

            #print statistics
            if(i%2000==0):
              print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {train_loss:.4f}')

learning_rate=0.01
num_epochs=3

optimizer=torch.optim.SGD(model.parameters(),lr=learning_rate)

train_network(train_loader,optimizer,criteria,num_epochs)
print('Training Completed')

device='cuda' if torch.cuda.is_available() else 'cpu'
print(device)

from torchmetrics import F1Score,Recall,Precision,Accuracy

"""# Testing the model"""

def test_model(test_loader,model,criteria):

    model.eval()
    test_loss,correct=0,0
    num_batches=len(test_loader)
    size=len(test_loader.dataset)

    with torch.no_grad():
        for X,y in test_loader:
            tmp=torch.nn.functional.one_hot(y,num_classes=10)
            outputs=model(X)

            test_loss=test_loss+criteria(outputs,tmp).item()
            correct=correct+(outputs.argmax(1)==y).type(torch.float).sum().item()
            
    test_loss=test_loss/num_batches
    correct=correct/size

    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

    accuracy = Accuracy()
    #print('Accuracy: ',accuracy(outputs,y))

    precision=Precision(average='macro',num_classes=10)
    #print(f'Precision:{precision(outputs,y)}')

    recall=Recall(average='macro',num_classes=10)
    #print(f'Precision:{recall(outputs,y)}')

    f1_score=F1Score(average='macro',num_classes=10)
    #print(f'Precision:{f1_score(outputs,y)}')

    return accuracy(outputs,y).item(), precision(outputs,y).item(), recall(outputs,y).item(), f1_score(outputs,y).item()

"""# Metrics for checking the performance of model while testing"""

a,p,r,f1=test_model(test_loader,model,criteria)
print('Testing finished')

print(f'accuracy: {a:.4f}')
print(f'precision: {p:.4f}')
print(f'recall: {r:.4f}')
print(f'F1 score: {f1:.4f}')

# finding the input size and output size for each layer

# dataiter=iter(train_loader)
# images,labels=dataiter.next()

# conv1=nn.Conv2d(1,6,5)
# pool=nn.MaxPool2d(2,2)
# conv2=nn.Conv2d(6,16,5)
# print(images.shape)


# x=conv1(images)
# print(x.shape)

# x=pool(x)
# print(x.shape)

# x=conv2(x)
# print(x.shape)

# x=pool(x)
# print(x.shape)





