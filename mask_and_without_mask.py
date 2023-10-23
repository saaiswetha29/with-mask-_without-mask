# -*- coding: utf-8 -*-
"""mask and without mask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_CCZUsOlRz3Q0KEvixIPTb73QKdg8UcD
"""

from google.colab import drive
drive.mount('/content/drive')

!unzip "/content/drive/MyDrive/archive.zip"

"""# import library"""

import cv2
from google.colab.patches import cv2_imshow
import numpy as np
import pandas as pd
from tensorflow.keras.layers import Dense,Flatten,Conv2D,MaxPooling2D,BatchNormalization,Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import image_dataset_from_directory
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

with_mask_path="/content/data/with_mask"
without_mask_path="/content/data/without_mask"

"""# split folders"""

!pip install split-folders
import splitfolders

direction="/content/data"
splitfolders.ratio(direction, output="splitted_data", seed=22, ratio=(0.7,0.3))

train_path="/content/splitted_data/train"
val_path="/content/splitted_data/val"

train_data = image_dataset_from_directory(
    directory = '/content/splitted_data/train',
    labels='inferred',
    label_mode = 'binary',
    batch_size=32,
    image_size=(256,256)
)

val_data =image_dataset_from_directory(
    directory = '/content/splitted_data/val',
    labels='inferred',
    label_mode = 'binary',
    batch_size=32,
    image_size=(256,256)
)

train_data.class_names

"""# train the model"""

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())

model.add(Dense(128,activation='relu'))

model.add(Dense(64,activation='relu'))

model.add(Dense(1,activation='sigmoid'))

model.compile(loss="binary_crossentropy",optimizer="adam",metrics=["accuracy"])

History=model.fit(train_data,validation_data=val_data,epochs=5)

import matplotlib.pyplot as plt

plt.plot(History.history['accuracy'],color='red',label='train')
plt.plot(History.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

data_augmentation = keras.Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal",
                                                 input_shape=(256,256,
                                                              3)),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomZoom(0.2),
  ]
)

model1 = Sequential()

model1.add(data_augmentation)

model1.add(Conv2D(32,kernel_size=(3,3),padding='same',activation='relu'))
model1.add(BatchNormalization())
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Conv2D(64,kernel_size=(3,3),padding='same',activation='relu'))
model1.add(BatchNormalization())
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Conv2D(64,kernel_size=(3,3),padding='same',activation='relu'))
model1.add(BatchNormalization())
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu'))
model1.add(BatchNormalization())
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Conv2D(128,kernel_size=(3,3),padding='same',activation='relu'))
model1.add(BatchNormalization())
model1.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model1.add(Flatten())

model1.add(Dense(128,activation='relu'))
model1.add(Dropout(0.2))
model1.add(Dense(64,activation='relu'))
model1.add(Dropout(0.2))
model1.add(Dense(64,activation='relu'))
model1.add(Dropout(0.2))
model1.add(Dense(32,activation='relu'))
model1.add(Dropout(0.1))
model1.add(Dense(1,activation='sigmoid'))


model1.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history1 = model1.fit(train_data,epochs=5,validation_data=val_data)

plt.plot(history1.history['accuracy'],color='red',label='train')
plt.plot(history1.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

"""# predict image"""

from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

def predict_image(img_path):
  img=image.load_img(img_path,target_size=(256, 256))
  img_array=image.img_to_array(img)
  img_batch=np.expand_dims(img_array,axis=0)
  result=model1.predict(img_batch)
  plt.imshow(img)
  plt.axis('off')  # Remove axes
  plt.show()
  if result>=0.5:
    return("without_mask")
  else:
    return("with_mask")

predict_image("/content/mask1.jpg")

predict_image("/content/without_mask.jpg")

predict_image("/content/mask_1.jpg")

predict_image("/content/without_2.jpeg")

"""# save the model"""

model1.save("cnn_with_mask_without_mask.h5")