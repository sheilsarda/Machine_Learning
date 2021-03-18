# -*- coding: utf-8 -*-
"""CIS520_hw4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bqsmo8EeXs2n9BJ-jj5mvPWyLNx7n0yv

# Homework 4: Coding

**Due Monday October 12th, 11:59pm.**


**In order to avoid module version issues, please complete this assignment on Colab.**

**Submit hw4.py file to Gradescope (note there is no autograder for this assignment).**
"""

"""
Import libraries that you might require
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import operator
from sklearn.metrics import accuracy_score
import sklearn.model_selection as ms


from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

"""
Load data (MNIST digits dataset).

Note that we will skip the validation phase for
this exercise as by now you are pretty familiar with the typical Machine Learning
pipeline.
"""

from sklearn.datasets import load_digits
digits = load_digits()
print(digits.data.shape)

X = digits['data']
y = digits['target']

np.random.seed(100)
p = np.random.permutation(len(X))
X, y = X[p], y[p]

X_train, y_train = X[:1500], y[:1500]
X_test, y_test = X[1500:], y[1500:]

"""# Question 2: Performance Comparisons for three ML algorithms

## 2.0 Accuracy
"""

def train(models, X_train, y_train, X_test, y_test):
    """
    Trains several models and returns the test accuracy for each of them
    Args:
      models: list of model objects
    Returns:
      score (float): list of accuracies of the different fitted models on test set
    """
    
    # Train and test each model in a for lop
    accuracies = []
    
    for model in models:
        clf = model.fit(X_train, y_train) # Train
        score = clf.score(X_test, y_test) # Test
        accuracies.append(score)

    return accuracies

"""## 2.1 Random Forest Classifier"""

def modelRF(n_estimators):
    """
    Creates model objects for the Random Forest Classifier.
    See the documentation in sklearn here:
    https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
    Args:
    n_estimators: list of hyper parameters
    return:
    list of classifiers
    """
  
    list_n_estimators = n_estimators
    random_state = 20 # Do not change this random_state

    objs_RFC = []

    # Create a list of objects for the classifier for each of the above "n_estimators"
    for n_est in list_n_estimators:
        rf = RandomForestClassifier(n_estimators=n_est, random_state=random_state)
        objs_RFC.append(rf)
    
    return objs_RFC


# call the above function to train and test the Random Forest Classifier
n_estimators = [1, 5, 10, 50, 100, 500]
RF_models = modelRF(n_estimators=n_estimators)
RF_accuracies = train(RF_models, X_train, y_train, X_test, y_test)
for est, acc in zip(n_estimators, RF_accuracies):
    print('Accuracy of %5s : %2d %%' % (
        est, acc*100))

"""## 2.2 Kernel SVM"""

def modelKSVM():
    """
    Creates model objects for the Kernel SVM.
    See the documentation in sklearn here:
    https://scikit-learn.org/stable/modules/svm.html
    """

    list_kernel_type = ['linear', 'poly', 'rbf']
    random_state = 20 # Do not change this random_state

    objs_KSVM = []

    # Create a list of objects for the classifier for each of the above "kernel" types
    for kernel in list_kernel_type:
        svm = SVC(kernel=kernel, random_state=random_state)
        objs_KSVM.append(svm)

    return objs_KSVM

# Call the above function to train and test the Kernel SVM
KSVM_models = modelKSVM()
list_kernel_type = ['linear', 'poly', 'rbf']
KSVM_accuracies = train(KSVM_models, X_train, y_train, X_test, y_test)
for est, acc in zip(list_kernel_type, KSVM_accuracies):
    print('Accuracy of %5s : %2d %%' % (
        est, acc*100))

"""## 2.3 Multi Layer Perceptron"""

def modelMLP():
    """
    Creates model objects for the Multi Layered Perceptron.
    See the documentation in sklearn here:
    https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html
    """
    
    layerSizes = [(3), (10), (10,10,10), (20,50,20)]
    random_state = 20 # Do not change this random_state
    max_iter = 2000 # fixed max_iter

    objs_MLP = []

    # Create a list of objects for the classifier for each of the above "layerSizes"
    for size in layerSizes:
        mlp = MLPClassifier(hidden_layer_sizes=size, max_iter=max_iter, random_state=random_state)
        objs_MLP.append(mlp)

    return objs_MLP

# Call the above function to train and test the Multi Layer Perceptron
MLP_models = modelMLP()
layerSizes = [(3), (10), (10,10,10), (20,50,20)]
MLP_accuracies = train(MLP_models, X_train, y_train, X_test, y_test)
for est, acc in zip(layerSizes, MLP_accuracies):
    print('Accuracy of %5s : %2d %%' % (
        est, acc*100))

"""## 2.4 AdaBoost"""

def modelAdaBoost():
    """
    Creates model objects for the AdaBoost.
    See the documentation in sklearn here:
    https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html
    """
    num_estimators = [1,5,10,50,100,150]
    learning_rate = 0.1
    max_depth = 3
    base_estimate = DecisionTreeClassifier(max_depth=max_depth)
    random_state = 20 # Do not change this random_state
    
    obj_boost = []
    
    """ 
    Create a list of objects for the classifier 
    for each of combination of above num_estimators and learning_rate
    """
    for n_est in num_estimators:
        boost = AdaBoostClassifier(n_estimators=n_est, 
                                   learning_rate=learning_rate, 
                                   base_estimator = base_estimate, 
                                   random_state =random_state)
        obj_boost.append(boost)

    return obj_boost

# Call the above function to train and test the AdaBoost Classifier
Ada_models = modelAdaBoost()
num_estimators = [1,5,10,50,100,150]
Ada_accuracies = train(Ada_models, X_train, y_train, X_test, y_test)
for est, acc in zip(num_estimators, Ada_accuracies):
    print('Accuracy of %5s : %2d %%' % (
        est, acc*100))

"""# Question 3.2 Convolutional Neural Networks  
In this assignment you will be training a Convolutional Neural Network on  
the Fashion MNIST dataset.  

You may find more information about the dataset [here](https://github.com/zalandoresearch/fashion-mnist).  
For this assignment we have already loaded the dataset for you.  
  
You will be using PyTorch for implementing your CNN. 

**We highly recommend following [this tutorial](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py) for this question** as well as referring to the [official documentation](https://pytorch.org/docs/stable/nn.html) if you are unfamiliar with Pytorch.

## Setup: Load Tensorboard

The below code is used to load [Tensorboard](https://www.tensorflow.org/guide/summaries_and_tensorboard), which is used to visualize the training and execution of your neural network.

Run the below cells and click on the Tensorboard link produced by the third cell below while your network is training (Section 3.2.5) to plot the accuracy and loss curves.
"""

!rm -r -f ./logs
import datetime
 
LOG_DIR = "./logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
get_ipython().system_raw(
    'tensorboard --logdir {} --host 0.0.0.0 --port 6006 &'
    .format(LOG_DIR)
)

!if [ -f ngrok ] ; then echo "Ngrok already installed" ; else wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip > /dev/null 2>&1 && unzip ngrok-stable-linux-amd64.zip > /dev/null 2>&1 ; fi

get_ipython().system_raw('./ngrok http 6006 &')

! curl -s http://localhost:4040/api/tunnels | python3 -c \
    "import sys, json; print('Tensorboard Link: ' +str(json.load(sys.stdin)['tunnels'][0]['public_url']))"

# %load_ext tensorboard 
# %tensorboard --logdir logs
# logger = Logger(logdir)

"""## Setup: Logger

Please look at the functions the logger class provides. You may use them to log   
training metrics like loss, accuracy and even some selected images and their  
labels to see how network parameters change during training.
"""

# Code referenced from https://gist.github.com/gyglim/1f8dfb1b5c82627ae3efcfbbadb9f514
import tensorflow as tf
import numpy as np
import scipy.misc 
try:
    from StringIO import StringIO  # Python 2.7
except ImportError:
    from io import BytesIO         # Python 3.x


class Logger(object):
    
    def __init__(self, log_dir):
        """Create a summary writer logging to log_dir."""
        self.writer = tf.summary.create_file_writer(log_dir)

    def scalar_summary(self, tag, value, step):
        """Log a scalar variable."""
        with self.writer.as_default():
            tf.summary.scalar(name=tag, data=value, step=step)
        self.writer.flush()

    def image_summary(self, tag, images, step):
        """Log a list of images."""

        for i, img in enumerate(images):
            # Write the image to a string
            try:
                s = StringIO()
            except:
                s = BytesIO()
            scipy.misc.toimage(img).save(s, format="png")

            # Create an Image object as a Summary value
            with self.writer.as_default():
                tf.summary.image(name='%s/%d' % (tag, i), data=s.getvalue(), step=step)

        # Create and write Summary
        self.writer.flush()
        
    def histo_summary(self, tag, values, step, bins=1000):
        """Log a histogram of the tensor of values."""

        # Create a histogram using numpy
        counts, bin_edges = np.histogram(values, bins=bins)

        # Fill the fields of the histogram proto
        hist = tf.HistogramProto()
        hist.min = float(np.min(values))
        hist.max = float(np.max(values))
        hist.num = int(np.prod(values.shape))
        hist.sum = float(np.sum(values))
        hist.sum_squares = float(np.sum(values**2))

        # Drop the start of the first bin
        bin_edges = bin_edges[1:]

        # Add bin edges and counts
        for edge in bin_edges:
            hist.bucket_limit.append(edge)
        for c in counts:
            hist.bucket.append(c)

        # Create and write Summary
        with self.writer.as_default():
            tf.summary.histogram(name=tag, data=hist, step=step)
        self.writer.flush()
logger = Logger('./logs')

import torch
import torchvision
from torchvision import datasets, transforms

"""##3.2.1 Loading the Dataset
The output of torchvision datasets are PILImage images of range [0, 1].  
We transform them to Tensors of normalized range [-1, 1].  
```Transforms.Normalize((mean,),(std,))``` basically manipulates the values of a pixel such that  
$$New\_Value = \frac{Old\_Value - Mean}{Std}$$
"""

# Define a transform to normalize the data

# Set the value of mean and the standard deviation to 
# normalize the image from range [0,1] to the range [-1, 1]


#Begin Your Code

mean = 0.5
std = 0.5

#End Your Code

transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((mean,), (std,))
                                ])


# Select suitable value of batch_sizes.

#Begin Your Code

train_batch_size = 30
test_batch_size = 30

#End Your Code

# Download and load the training data
trainset = datasets.FashionMNIST('~/.pytorch/F_MNIST_data/', download=True, train=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=train_batch_size, shuffle=True)

# Download and load the test data
testset = datasets.FashionMNIST('~/.pytorch/F_MNIST_data/', download=True, train=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=test_batch_size, shuffle=True)


# Classes
classes = {       0 :'T-shirt/top',
                  1 :'Trouser',
                  2 :'Pullover',
                  3 :'Dress',
                  4 :'Coat',
                  5 :'Sandal',
                  6 :'Shirt',
                  7 :'Sneaker',
                  8 :'Bag',
                  9 :'Ankle boot'}

"""##3.2.2 The Dataset
Here we show some images of the dataset.  
See how many of the categories can you recognise.
"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

# Functions to show an image


def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    
    figure(num=None, figsize=(8, 6), dpi=150, edgecolor='k')
    plt.axis('off')
    plt.imshow(np.transpose(npimg, (1, 2, 0)))


# get some random training images
dataiter = iter(trainloader)
images, labels = dataiter.next()

# show images
imshow(torchvision.utils.make_grid(images))

"""##3.2.3 Create your Convolutional Neural Network
Create the CNN with layers and hyperparameter sets as mentioned in the LaTeX pdf for full credit.  
You are, however, free to change the architecture as long as you achieve accuracy better than the architecture shown in the LaTeX pdf.
"""

import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # Design your network, you are allowed to explore your own architecture
        # But you should achieve a better overall accuracy than the baseline network.
        # Also, if you do design your own network, include an explanation 
        # for your choice of network and how it may be better than the 
        # baseline network in your latex.
        
        #Begin Your Code
        # Layer 1
        self.conv1 = nn.Conv2d(in_channels = 1, out_channels=32, 
                               kernel_size=(5, 5), stride=1, padding = 2)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=32, 
                               kernel_size=(5, 5), stride=1, padding = 2)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, 
                               kernel_size=(5, 5), stride=1, padding = 2)

        self.batch1 = nn.BatchNorm2d(1)
        self.batch2 = nn.BatchNorm2d(32)        
        self.batch3 = nn.BatchNorm2d(32)

        self.pool1 = nn.MaxPool2d(2)
        self.pool2 = nn.MaxPool2d(2)
        self.pool3 = nn.MaxPool2d(2)
        
        self.batch4 = nn.BatchNorm2d(64)
        self.batch5 = nn.BatchNorm2d(10)

        self.fully_conn1 = nn.Linear(in_features = 64*7*7, 
                                out_features = 64)
        self.fully_conn2 = nn.Linear(in_features = 32*7*7, 
                                out_features = 10)
        
        self.softmax1 = nn.Softmax()
        self.relu = nn.ReLU(inplace=True)
        self.flatten = nn.Flatten()

        #End Your Code

    def forward(self, x):

      # Implement the forward function that applies the layers you have created to the input

      #Begin Your Code

      x = self.conv1(x)
      x = self.relu(x)
      x = self.pool1(x)

      x = self.conv2(x)
      x = self.relu(x)
      x = self.pool2(x)

      out = self.flatten(x)
      out = F.dropout(out, p = 0.5, training=True, inplace=True)
      out = self.fully_conn2(out)

      return out


net = Net()

      #End Your Code
net = Net()

"""##3.2.4 Define a Loss function and optimizer
We will be using [Cross Entropy Loss](https://pytorch.org/docs/stable/nn.html?highlight=crossentropyloss#torch.nn.CrossEntropyLoss) and [Adam optimizer](https://pytorch.org/docs/stable/optim.html?highlight=adam#torch.optim.Adam).  
Note: PyTorch's CrossEntropyLoss combines log softmax and negative log likelihood loss in one class. Make sure you are not computing softmax twice.
"""

import torch.optim as optim

# Use appropriate loss criterion and optimizer 

#Begin Your Code

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr = 0.001)

#End Your Code

"""##3.2.5. Train the network

Here we are going to train the network while logging the per batch metrics.  
This would take some time to run (5-10 minutes).
"""

overall_step = 0

# Select appropriate number of epochs

#Begin Your Code

epochs = 25

correct = 0
total = 0
#End Your Code


for epoch in range(epochs):  # loop over the dataset multiple times
    running_loss = 0
    for i, data in enumerate(trainloader, 0):
        # get the inputs
        inputs, labels = data

        # Make predictions, calculate accuracy and update your weights once

        # Begin Your Code

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        pred = net(inputs)
        loss = criterion(pred, labels)

        pred_result = pred.argmax(dim = 1)

        loss.backward()
        optimizer.step()

        correct += pred_result.eq(labels).float().sum()
        total += train_batch_size
        accuracy = correct / total

        #End Your Code

        # print statistics
        running_loss += loss.item()
        if i % 200 == 199:    # print every 200 mini-batches
            print('Epoch: %d, Batch: %5d, loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 200))
            running_loss = 0.0
            #Any thing that is added to the "info" gets plotted in tensorboard
            #TODO : Add the plots in Tensorboard to the report and explain what is happening
            info = {'loss' : loss.item(), 'accuracy': accuracy.item()}
            for tag, value in info.items():
                logger.scalar_summary(tag, value, overall_step+1)
                overall_step += 1 

print('Finished Training')

"""##3.2.6 Test Accuracy
Let us look at how the network performs on the test dataset.  
Report your accuracy in your report.
"""

correct = 0
total = 0
net.eval()
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

#TODO : Report this accuracy in your report.

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))

"""##3.2.7 Per Class accuracy
Now we see the test accuracy for each class in the test dataset.  
Report these accuracies in your report. Also identify the problematic classes.  
Can you explain why these classes have significantly lower accuracies compared to other classes? Record your responses in your LaTeX file.
"""

class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1


for i in range(10):
    print('Accuracy of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))

"""# Turning it in

**This notebook will not be autograded, so no need to comment out code outside of functions.**

1. Download this notebook as a `hw4.py` file with the functions implemented and the sandbox code commented out
  - go to "File -> Download .py"
  
2. Submit `hw4.py` file to Gradescope (you can do this as many times as you'd like before the deadline)
"""