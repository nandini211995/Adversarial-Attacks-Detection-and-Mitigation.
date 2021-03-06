# -*- coding: utf-8 -*-
"""DAI_Assignment2_Q1(A)withVGG.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1au2XIXxQNqnZ95h2XNy2X0gdnVqsEnb0
"""

!unzip /content/drive/MyDrive/dataset_DAI/D_10_Dataset.zip

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

directory = r'/content/Images/'
images = []
labels = []
labels_name = []

cnt = 0
for foldername in os.listdir(directory):
    for filename in os.listdir(directory + foldername):
        labels_np = np.zeros(10)
        ext=[".jpg",".jpeg"] 
        if filename.endswith(tuple(ext)):
            img = cv2.imread(os.path.join(directory,foldername, filename))
            if img is not None:
                resized_im = cv2.resize(img, (64, 64))
                images.append(resized_im)
                labels_np[cnt] = 1
                labels.append(labels_np)
    cnt +=1
    labels_name.append(foldername)

tmp= images[10].reshape((64,64,3))
plt.imshow(tmp)
plt.show()

data_images = np.asarray(images)
data_images.shape

labels_images = np.asarray(labels)
labels_images.shape

x_data = data_images.astype('float16')
x_data /= 255.

from sklearn.model_selection import train_test_split
x_train, x_test,y_train,y_test = train_test_split(x_data,labels_images,test_size=0.2, random_state=20)

x_train.shape

x_test.shape

"""#VGG16 Deep Model"""

# Importing the required libraries
import tensorflow as tf
import keras
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

# Initializing a Sequential model
model = Sequential()

# Creating first block- (2 Convolution + 1 Max pool)
model.add(Conv2D(filters= 64, kernel_size= (3,3), strides= (1,1), padding='same', input_shape= (64, 64, 3), activation= 'relu'))
model.add(Conv2D(filters= 64, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(MaxPool2D(pool_size= (2,2), strides=(2,2)))

# Creating second block- (2 Convolution + 1 Max pool)
model.add(Conv2D(filters= 128, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 128, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(MaxPool2D(pool_size= (2,2), strides=(2,2)))

# Creating third block- (3 Convolution + 1 Max pool)
model.add(Conv2D(filters= 256, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 256, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 256, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(MaxPool2D(pool_size= (2,2), strides=(2,2)))

# Creating fourth block- (3 Convolution + 1 Max pool)
model.add(Conv2D(filters= 512, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 512, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 512, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(MaxPool2D(pool_size= (2,2), strides=(2,2)))

# Creating fifth block- (3 Convolution + 1 Max pool)
model.add(Conv2D(filters= 512, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 512, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(Conv2D(filters= 512, kernel_size= (3,3), strides= (1,1), padding='same', activation= 'relu'))
model.add(MaxPool2D(pool_size= (2,2), strides=(2,2)))

# Flattening the pooled image pixels
model.add(Flatten())

# Creating 2 Dense Layers
model.add(Dense(units= 4096, activation='relu'))
model.add(Dense(units= 4096, activation='relu'))

# Creating an output layer
model.add(Dense(units= 10, activation='softmax'))

model.summary()

temhist = model.load_weights("/content/drive/MyDrive/VGG16_ASS2/main_vgg16_23_1_2021_weight.h5")

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=3, verbose=1, validation_data=(x_test, y_test))

df = pd.read_csv('/content/drive/MyDrive/VGG16_ASS2/vgg16_64_23012021_history.csv')

df

loss_train = df['loss']
loss_test = df['val_loss']
epochs = range(1,13)
plt.plot(epochs, loss_train, 'g', label='Training loss')
plt.plot(epochs, loss_test, 'b', label='Testing loss')
plt.title('Training and Testing loss with VGG16')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

loss_test, accuracy_test = model.evaluate(x_test, y_test)
print('Accuracy on test data: {:4.2f}%'.format(accuracy_test * 100))

from sklearn.metrics import classification_report
from sklearn import metrics

ynew = model.predict(x_test)

ynew

pred_test_labels_new = np.argmax(ynew,axis=1)

pred_test_labels_new

from keras.utils import to_categorical
pred_test_labels = to_categorical(pred_test_labels_new, dtype='float16',num_classes=10)

pred_test_labels

y_test

print(f"Classification report for VGG16:\n"
      f"{classification_report(y_test, pred_test_labels)}\n")