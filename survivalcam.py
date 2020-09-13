# -*- coding: utf-8 -*-
"""survivalcam.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_u81Cc_R56XW5-2zm86DLr_3RcTnOS-a
"""

!cp "/content/drive/My Drive/survcam/class.zip" "survdata.zip"

!unzip -q survdata.zip

import sys
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

import matplotlib.pyplot as plt

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout, Activation, Concatenate, Flatten, MaxPooling2D, Convolution2D, Convolution1D, MaxPooling1D, GlobalMaxPooling1D, BatchNormalization, LSTM, GRU, Bidirectional
from keras.regularizers import l2,l1
from keras.optimizers import SGD,Adam,RMSprop
from tensorflow.compat.v1 import InteractiveSession
import keras.backend as K
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from keras.callbacks import EarlyStopping, ModelCheckpoint,ReduceLROnPlateau
from keras.models import load_model

import keras

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

import tensorflow as tf
print(tf.__version__)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from keras.utils import to_categorical, plot_model

class0 = os.listdir('class0')
class1 = os.listdir('class1')

len(class0),len(class1)

#constructing label
label_0 = np.zeros((212,1))
label_1 = np.ones((215,1))

label = np.concatenate((label_0,label_1),axis=0)

label.shape

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

Y = le.fit_transform(label).reshape(-1,1)
Y.shape

samples = 427

dims = (123,123)
#ideal 4x28
#actual 54x390
shape_0 = (212, dims[0], dims[1], 1)
shape_1 = (215, dims[0], dims[1], 1)     

dataset_0 = np.zeros(shape=shape_0,dtype=np.float32)
dataset_1 = np.zeros(shape=shape_1,dtype=np.float32)

dataset_0.shape, dataset_1.shape

#load off-target images
i=0
for item_0 in class0:
    img0 = load_img('class0/'+ item_0, target_size=dims, color_mode='grayscale',interpolation='nearest')  # this is a PIL image
    # Convert to Numpy Array
    x0 = img_to_array(img0)
    dataset_0[i] = x0
    i += 1
    if i % 100 == 0:
        print("%d images to array" % i)

print("All class_0 images done!")

j=0
for item_1 in class1:
    img1 = load_img('class1/'+ item_1, target_size=dims, color_mode='grayscale',interpolation='nearest')  # this is a PIL image
    # Convert to Numpy Array
    x1 = img_to_array(img1)
    dataset_1[j] = x1
    j += 1
    if j % 100 == 0:
        print("%d images to array" % j)

print("All class_1 images done!")

dataset_0.shape, dataset_1.shape

dataset = np.concatenate((dataset_0,dataset_1),axis=0)

dataset.shape, Y.shape

dataset_train, dataset_test, Y_train, Y_test, = train_test_split(dataset, Y,test_size=0.2, random_state=0)

indices = list(range(0,427))
indices_train,indices_test = train_test_split(indices, test_size=0.2, random_state=0)

dataset_train.shape, dataset_test.shape, Y_train.shape, Y_test.shape

from keras import backend as K
K.clear_session()

import gc
gc.collect()

#now model
try:
  del model, history
except:
  pass

#model
input_1  = Input(shape = (123,123,1))
conv_1   = Convolution2D(512, (3, 3), kernel_initializer='glorot_normal')(input_1)
bn_1     = BatchNormalization()(conv_1)
act_1    = Activation('relu')(bn_1)
pool_1   = MaxPooling2D(pool_size = (2,2))(act_1)

conv_2   = Convolution2D(512, (3, 3), kernel_initializer='glorot_normal')(pool_1)
bn_2     = BatchNormalization()(conv_2)
act_2    = Activation('relu')(bn_2)
pool_2   = MaxPooling2D(pool_size = (2,2))(act_2)

conv_3   = Convolution2D(512, (3, 3), kernel_initializer='glorot_normal')(pool_2)
bn_3     = BatchNormalization()(conv_3)
act_3    = Activation('relu')(bn_3)
pool_3   = MaxPooling2D(pool_size = (2,2))(act_3)

flatten = Flatten()(pool_3)

dense_1 = Dense(512, activation = 'relu',kernel_initializer='glorot_normal')(flatten)
dense_1_dropout = Dropout(0.5)(dense_1)
dense_2 = Dense(256, activation = 'relu',kernel_initializer='glorot_normal')(dense_1_dropout)
dense_2_dropout = Dropout(0.2)(dense_2)
dense_3 = Dense(128, activation = 'relu',kernel_initializer='glorot_normal')(dense_2_dropout)
output   = Dense(1, activation = 'sigmoid')(dense_3)

model = Model(inputs=input_1, outputs=output)

model.summary()

metrics = [
    keras.metrics.BinaryAccuracy(name='accuracy'),
    keras.metrics.Precision(name="precision"),
    keras.metrics.Recall(name="recall"),
    keras.metrics.AUC(name="auc")
]

model.compile(optimizer=keras.optimizers.Adam(lr=0.0001),loss='binary_crossentropy',metrics=metrics)

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5,patience=5, min_lr=0.00000001, verbose=1)

early_stopping = EarlyStopping(monitor='val_accuracy', patience=10,restore_best_weights=True, verbose=1)

history=model.fit(dataset_train, Y_train, 
                batch_size=32, 
                epochs=40, 
                verbose=1,
                validation_data=(dataset_test,Y_test),
                #validation_split=0.1,
                callbacks=[reduce_lr,early_stopping],
                )

model.save('model_latest.hdf5')

!cp "model_latest.hdf5" "/content/drive/My Drive/survcam/"

# predict on test set
Y_pred = model.predict(dataset_test)

#plots
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc

fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(1):
    fpr[i], tpr[i], _ = roc_curve(Y_test[:, i], Y_pred[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plot of a ROC curve for a specific class
fig, ax = plt.subplots(figsize=(8,7))
ax.plot(fpr[0], tpr[0],label=' (AUC: %0.2f)' % roc_auc[0], alpha=1)
ax.plot([0, 1], [0, 1], 'k--')
ax.set_ylim([0.0, 1.01])
ax.set_xlim([0.0, 1.01])
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_xticks(np.arange(0, 1.1, 0.1))
ax.set_xlabel('False Positive Rate', fontsize=14)
ax.set_ylabel('True Positive Rate', fontsize=14)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12) 
ax.grid()
ax.legend(fontsize=12)
plt.savefig('roc.png', dpi=500, bbox_inches='tight')

precision = dict()
recall = dict()
average_precision = dict()
for i in range(1):
    precision[i], recall[i], _ = precision_recall_curve(Y_test[:, i], Y_pred[:, i])
    average_precision[i] = average_precision_score(Y_test[:, i], Y_pred[:, i])

# A "micro-average": quantifying score on all classes jointly
precision["micro"], recall["micro"], _ = precision_recall_curve(Y_test.ravel(), Y_pred.ravel())
average_precision["micro"] = average_precision_score(Y_test, Y_pred, average="micro")
#print('Average precision score , micro-averaged over all classes: {0:0.2f}'
#    .format(average_precision["micro"]))

fig, ax = plt.subplots(figsize=(8,7))
ax.step(recall['micro'], precision['micro'], where='post')

ax.set_xlabel('Recall', fontsize=14)
ax.set_ylabel('Precision', fontsize=14)
ax.plot([0, 1], [1, 0], 'k--')
ax.set_ylim([0.0, 1.01])
ax.set_xlim([0.0, 1.00])
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_xticks(np.arange(0, 1.1, 0.1))
ax.set_title('AP={0:0.2f}'.format(average_precision["micro"]), fontsize=14)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12) 
ax.grid(linestyle='-.', linewidth=0.7)
plt.savefig('aupr.png', dpi=500, bbox_inches='tight')

#confusion matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn import metrics as sklearn_metrics

y_label_pred = np.where(Y_pred > 0.5, 1, 0)

print(sklearn_metrics.confusion_matrix(Y_test, y_label_pred))

tn, fp, fn, tp = sklearn_metrics.confusion_matrix(Y_test, y_label_pred).ravel()
print(tn, fp, fn, tp)

print(sklearn_metrics.classification_report(Y_test, y_label_pred, digits=3))

#gradcams

!pip install tf-keras-vis

from tf_keras_vis.utils import num_of_gpus

_, gpus = num_of_gpus()
print('{} GPUs'.format(gpus))

Y_pred.shape

print(indices_test)
print(Y_pred)

#indices to check
#class_1 =  8,17,20
#class_0 =  85,76,75

print(indices_test[8],indices_test[17],indices_test[20])
print(indices_test[85],indices_test[76],indices_test[75])

cimg = dataset[124]

plt.imshow(cimg.squeeze(), cmap='gray')

def loss(output):
    return (output[0][0])

def model_modifier(m):
    m.layers[-1].activation = tf.keras.activations.linear
    return m

# Rendering
subplot_args = { 'nrows': 1, 'ncols': 1, 'figsize': (9, 3),
                 'subplot_kw': {'xticks': [], 'yticks': []} }

from tensorflow.keras import backend as K
from tf_keras_vis.saliency import Saliency
from tf_keras_vis.utils import normalize

saliency = Saliency(model,
                    model_modifier=model_modifier,
                    clone=True)

# Generate saliency map

saliency_map = saliency(loss, cimg)
saliency_map = normalize(saliency_map)

f, ax = plt.subplots(**subplot_args)
ax.imshow(saliency_map.squeeze(), cmap='jet')
ax.imshow(cimg.squeeze(), cmap='gray', alpha=0.5)
plt.tight_layout()
plt.show()

saliency_map = saliency(loss,
                        cimg,
                        smooth_samples=30, # The number of calculating gradients iterations.
                        smooth_noise=0.20) # noise spread level.
saliency_map = normalize(saliency_map)

f, ax = plt.subplots(**subplot_args)
ax.imshow(cimg.squeeze(), cmap='gray')
ax.imshow(saliency_map.squeeze(), cmap='jet', alpha=0.5)
plt.tight_layout()
plt.show()

#gradcam

model.layers

from tf_keras_vis.gradcam import Gradcam,GradcamPlusPlus

gradcam = GradcamPlusPlus(model,
                  model_modifier=model_modifier,
                  clone=True)

cam = gradcam(loss,
              cimg,
              penultimate_layer=5, # model.layers number
             )
cam = normalize(cam)

f, ax = plt.subplots(**subplot_args)
ax.imshow(cimg.squeeze(), cmap='gray')
ax.imshow(cam.squeeze(), cmap='jet', alpha=0.5) # overlay
plt.tight_layout()
plt.show()

#score cam

from tf_keras_vis.scorecam import ScoreCAM

scorecam = ScoreCAM(model, model_modifier, clone=True)

cam = scorecam(loss,
              cimg,
              penultimate_layer=-1, # model.layers number
             )
cam = normalize(cam)

f, ax = plt.subplots(**subplot_args)
#heatmap = np.uint8(cm.jet(cam)[..., :3] * 255)
ax.imshow(cimg.squeeze(), cmap='gray')
ax.imshow(cam.squeeze(), cmap='jet', alpha=0.5) # overlay
plt.tight_layout()
plt.show()
