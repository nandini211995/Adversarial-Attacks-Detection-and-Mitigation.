# Adversarial-Attacks-Detection-and-Mitigation.

This implementation contains the different types of Adversarial Attacks, Detection and Mitigation.

**Dataset** : [D10 dataset - 10 class animal dataset](https://drive.google.com/file/d/15zl0Ef0G_P_b-9akgIc67gQohU7dUmfy/view)

* In this work, I considered Deep Models (like VGG16, VGG19, ResNet50) and train the D-10
Dataset from scratch(no pre-initialized weights) and report the accuracy, training-testing loss
graph, classification report using sklearn library.

* It includes both targeted and untargeted attacks(on testing set) for 3 attacks, those are Fast gradient sign method , Carlini and Wagner attack and Jacobian-based saliency map approach.

* Also Report SSIM(Structural Similarity) for the predictions. 

* For the **attack detection** , here 3 measures used such as 1. Using Average Perturbation 2. Using SSIM measure 3. Using Universal Quality Image Index (UQI)that can be used as a metric to detect adversarial perturbation and compare the results.

* Next part is : Perturb all images in the training and testing set (using any 1 attack ), train the model with perturbed training set image and then perform 10-class classification. The classification report is provided and compare the training and testing
accuracy with the previous case. Report SSIM for this case too and a comparison also done with the results of 
the previous case.

* **Mitigation**: Here we used perturbed test images(from previous part) and perform JPEG compression
at 2 different compression rates, compare the classification report(for the model trained with
original image set) of this case with all 2 previous cases i.e. original test samples and perturbed
samples.
