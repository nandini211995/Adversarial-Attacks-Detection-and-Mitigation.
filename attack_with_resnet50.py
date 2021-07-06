# -*- coding: utf-8 -*-
"""AttackPartofDAI_Assignment2_Q1(B)_Res50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aEmc171Pq-swDDt0jDxi-WPlqHjqyX21
"""

pip install adversarial-robustness-toolbox
pip install sewar

import os
import cv2
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from art.estimators.classification import KerasClassifier
from art.estimators.classification import TensorFlowV2Classifier
from art.attacks.evasion import FastGradientMethod, CarliniLInfMethod,BasicIterativeMethod,SaliencyMapMethod

labels = ['pecora','cavallo','mucca','gallina','ragno','gatto','scoiattolo','elefante','cane','farfalla',]

"""#ResNet50 Deep Model"""

# Importing the required libraries
import tensorflow as tf
import keras
import pickle
import pandas as pd
import numpy as np
from keras.applications.resnet50 import ResNet50
from keras.models import Model
import keras

model = ResNet50(include_top=True,input_shape = (64, 64, 3), classes = 10, weights='/content/drive/MyDrive/res50_dai_ass2/res50_24_01_2021_img_size64.h5')

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])

"""Create a ART Keras classifier for the TensorFlow Keras model."""

loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()

classifier = TensorFlowV2Classifier(model=model, nb_classes=10, input_shape=(64, 64, 3), loss_object=loss_object, 
                                    clip_values=(0, 1), channels_first=False)

"""#Fast Gradient Sign Method attack

Create a ART Fast Gradient Sign Method Non Targeted attack.
"""

attack_fgsm = FastGradientMethod(estimator=classifier, eps=0.1,targeted = False)

#x_test_adv = attack_fgsm.generate(x_test)

with open('/content/drive/MyDrive/VGG16_ASS2/vgg_16_train.pickle', 'rb') as f:
    x_train_n, y_train_n = pickle.load(f)

with open('/content/drive/MyDrive/VGG16_ASS2/vgg_16_test.pickle', 'rb') as f:
    x_test_n, y_test_n = pickle.load(f)

with open('/content/drive/MyDrive/res50_dai_ass2/res50_x_test_adv_fgsmntar.pickle', 'rb') as f:
    x_test_adv_fgsm_nt = pickle.load(f)

plt.imshow((np.reshape(x_test_n[2175], (64,64,3)) * 255).astype(np.uint8))
plt.show()
y_test_n[2175]

loss_test_fgsm_nt, accuracy_test_fgsm_nt = model.evaluate(x_test_adv_fgsm_nt, y_test_n)
perturbation_fgsm_nt = np.mean(np.abs((x_test_adv_fgsm_nt - x_test_n)))
print('Accuracy of FGSM (untargeted)adversarial test data: {:4.2f}%'.format(accuracy_test_fgsm_nt * 100))
print('Average perturbation in FGSM (untargeted): {:4.2f}'.format(perturbation_fgsm_nt))

x_fgsmpert_ntr = x_test_adv_fgsm_nt[2].reshape(1,64,64,3)
x_ntr = x_test_n[2].reshape(1,64,64,3)

pred_fgsmadv_ntr = classifier.predict(x_fgsmpert_ntr)
label_fgsmadv_ntr = np.argmax(pred_fgsmadv_ntr, axis=1)[0]
label_fgsmadv_ntr

label_test_ntr = np.argmax(y_test_n, axis=1)[2]
label_test_ntr

test_pred = classifier.predict(x_ntr)
test_label = np.argmax(test_pred, axis=1)[0]
test_label

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[2], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow(x_test_adv_fgsm_nt[2].reshape((64,64,3)))
ax1.set_title("Model Prediction: {}".format(labels[test_label]))
ax2.set_title("Model Prediction with attack : {}".format(labels[label_fgsmadv_ntr]))
ax1.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
ax2.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
plt.show()

from skimage.measure import compare_ssim

(score, diff) = compare_ssim(x_test_n[2], x_test_adv_fgsm_nt[2], full=True, multichannel=True)
diff = (diff * 255).astype("uint8")
print("SSIM for FGSM untargted : {:4.2f}%".format(score*100))

"""Create a ART Fast Gradient Sign Method Targeted attack."""

target_label = 9

attack_fgsm_tr = FastGradientMethod(estimator=classifier, eps=0.2,targeted = True)

x_art = np.expand_dims(x_test_n[2], axis=0)

from keras import utils as np_utils
from keras.utils import to_categorical

# Generate the adversarial sample:
x_fgsmadv_tr = attack_fgsm_tr.generate(x_art, y = to_categorical([target_label]))

# And apply the classifier to it:
pred_fgsmadv = classifier.predict(x_fgsmadv_tr)

pred_fgsmadv

label_fgsmadv = np.argmax(pred_fgsmadv, axis=1)[0]

label_fgsmadv

confidence_adv = pred_fgsmadv[:, label_fgsmadv][0]

confidence_adv

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[2], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow(x_fgsmadv_tr.reshape((64,64,3)))
ax1.set_title("Model Prediction: {}".format(labels[test_label]))
ax2.set_title("Model Prediction with attack : {}".format(labels[label_fgsmadv]))
ax1.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
ax2.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
plt.show()

x_art_new = x_fgsmadv_tr.reshape(64,64,3)

(score_at, diff_at) = compare_ssim(x_test_n[2],x_art_new,full=True, multichannel=True)
diff_at = (diff_at * 255).astype("uint8")
print("SSIM for FGSM targted : {:4.2f}%".format(score_at*100))

"""#Carlini&Wagner Infinity-norm attack

Create a ART Carlini&Wagner Infinity-norm target attack
"""

attack_cw_tar = CarliniLInfMethod(classifier=classifier, eps=0.4, max_iter=10, learning_rate=0.02,targeted=True)

cw_target_label = 9

x_art_cw_tar = np.expand_dims(x_test_n[221], axis=0)

# Generate the adversarial sample:
x_cwadv_tr = attack_cw_tar.generate(x_art_cw_tar, y = to_categorical([cw_target_label]))

# And apply the classifier to it:
pred_cwadv = classifier.predict(x_cwadv_tr)

pred_cwadv

label_adv_cwtar = np.argmax(pred_cwadv, axis=1)[0]
label_adv_cwtar

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[221], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow(x_cwadv_tr.reshape((64,64,3)))
ax1.set_title("Model Prediction: {}".format(labels[test_label]))
ax2.set_title("Model Prediction with attack : {}".format(labels[label_adv_cwtar]))
ax1.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
ax2.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
plt.show()

x_art_new_cw = x_cwadv_tr.reshape(64,64,3)

(score_at_cwt, diff_at_cwt) = compare_ssim(x_test_n[221],x_art_new_cw,full=True, multichannel=True)
diff_at_cwt = (diff_at_cwt * 255).astype("uint8")
print("SSIM for C&W targted : {:4.2f}%".format(score_at_cwt*100))

"""Carlini&Wagner Untargeted attack"""

attack_cw_utar = CarliniLInfMethod(classifier=classifier, eps=0.6, max_iter=10, learning_rate=0.05,targeted=False)

x_art_cw_utar = np.expand_dims(x_test_n[221], axis=0)

# Generate the adversarial sample:
x_cwadv_utr = attack_cw_utar.generate(x_art_cw_utar)

# And apply the classifier to it:
pred_cwadv_ut = classifier.predict(x_cwadv_utr)

pred_cwadv_ut

label_adv_cwutar = np.argmax(pred_cwadv_ut, axis=1)[0]
label_adv_cwutar

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[221], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow(x_cwadv_tr.reshape((64,64,3)))
ax1.set_title("Model Prediction: {}".format(labels[test_label]))
ax2.set_title("Model Prediction with attack : {}".format(labels[label_adv_cwutar]))
ax1.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
ax2.set_xlabel("True Label : {}".format(labels[label_test_ntr]))
plt.show()

x_art_new_cw_ut = x_cwadv_utr.reshape(64,64,3)

(score_at_cwut, diff_at_cwut) = compare_ssim(x_test_n[221],x_art_new_cw_ut,full=True, multichannel=True)
diff_at_cwut = (diff_at_cwut * 255).astype("uint8")
print("SSIM for C&W untargted : {:4.2f}%".format(score_at_cwut*100))

"""#Jacobian Saliency Map Attack (JSMA)

JSMA Target Attack
"""

attack_jsma = SaliencyMapMethod(classifier=classifier, theta=0.2, gamma = 0.8)

target_label = 9

x_art_jsma = np.expand_dims(x_test_n[2175], axis=0)

# Generate the adversarial sample:
x_art_adv_jsma = attack_jsma.generate(x_art_jsma, y = to_categorical([target_label]))

# And apply the classifier to it:
pred_adv_jsma = classifier.predict(x_art_adv_jsma)

pred_adv_jsma

label_adv_jsma = np.argmax(pred_adv_jsma, axis=1)[0]
label_adv_jsma

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[2175], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow(x_art_adv_jsma.reshape((64,64,3)))
ax1.set_title("Model Prediction: {}".format(labels[0]))
ax2.set_title("Model Prediction with attack : {}".format(labels[label_adv_jsma]))
ax1.set_xlabel("True Label : {}".format(labels[0]))
ax2.set_xlabel("True Label : {}".format(labels[0]))
plt.show()

x_art_new_jsma = x_art_adv_jsma.reshape(64,64,3)

(score_at_jsma, diff_at_jsma) = compare_ssim(x_test_n[2175],x_art_new_jsma,full=True, multichannel=True)
diff_at_jsma = (diff_at_jsma * 255).astype("uint8")
print("SSIM for JSMA targted : {:4.2f}%".format(score_at_jsma*100))

"""JSMA Untarget Attack"""

attack_jsma_ut = SaliencyMapMethod(classifier=classifier, theta=0.2, gamma = 0.8)

x_art_jsma = np.expand_dims(x_test_n[2175], axis=0)

# Generate the adversarial sample:
x_art_adv_jsma_ut = attack_jsma_ut.generate(x_art_jsma)

# And apply the classifier to it:
pred_adv_jsma_ut = classifier.predict(x_art_adv_jsma_ut)

pred_adv_jsma_ut

label_adv_jsma_ut = np.argmax(pred_adv_jsma_ut, axis=1)[0]
label_adv_jsma_ut

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[2175], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow(x_art_adv_jsma.reshape((64,64,3)))
ax1.set_title("Model Prediction: {}".format(labels[0]))
ax2.set_title("Model Prediction with attack : {}".format(labels[label_adv_jsma_ut]))
ax1.set_xlabel("True Label : {}".format(labels[0]))
ax2.set_xlabel("True Label : {}".format(labels[0]))
plt.show()

x_art_new_jsma_ut = x_art_adv_jsma_ut.reshape(64,64,3)

(score_ut_jsma, diff_ut_jsma) = compare_ssim(x_test_n[2175],x_art_new_jsma_ut,full=True, multichannel=True)
diff_ut_jsma = (diff_ut_jsma * 255).astype("uint8")
print("SSIM for JSMA Untargted : {:4.2f}%".format(score_ut_jsma*100))

"""# Measures to detect adversarial perturbation

1. Average Perturbation calulcation
"""

Avg_perturbation = np.mean(np.abs((x_test_adv_fgsm_nt[2175] - x_test_n[2175])))

Avg_perturbation

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax1.imshow((np.reshape(x_test_n[2175], (64,64,3)) * 255).astype(np.uint8))
ax2.imshow((np.reshape(x_test_adv_fgsm_nt[2175], (64,64,3)) * 255).astype(np.uint8))
ax1.set_title("Original image")
ax2.set_title("Image with avg peturbation : {}".format(Avg_perturbation))
ax1.set_xlabel("True Label : {}".format(labels[0]))
ax2.set_xlabel("True Label : {}".format(labels[0]))
plt.show()

"""2. Using SSIM measure i.e. Perturbation = 1 - SSIM"""

detect_x = np.array(x_test_adv_fgsm_nt[2175].reshape(64,64,3))

(score, diff) = compare_ssim(x_test_n[2175],detect_x,full=True, multichannel=True)
diff = (diff * 255).astype("uint8")
print("Perturbation using SSIM : {:4.2f}".format((1-score)))

""" 3. Universal Quality Image Index (UQI)"""

from sewar.full_ref import uqi
uqi_val = uqi(x_test_n[2175],detect_x)
uqi_val
print("Perturbation using UQI :",(1-uqi_val))

"""# Mitigation : JPEG compression"""

from art.defences.preprocessor import JpegCompression

miti = JpegCompression(clip_values = (0,1),quality=25)

compres25_test_data = miti(x_test_adv_fgsm_nt)

miti2 = JpegCompression(clip_values = (0,1),quality=50)

compres50_test_data = miti2(x_test_adv_fgsm_nt)

import pickle
with open('/content/drive/MyDrive/res50_dai_ass2/compJPEG25.pickle', 'wb') as f:
     pickle.dump(compres25_test_data, f)

with open('/content/drive/MyDrive/res50_dai_ass2/compJPEG50.pickle', 'wb') as f:
     pickle.dump(compres50_test_data, f)