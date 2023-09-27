# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:17:19 2022

@author: schomsin
"""

"""
Title: Image segmentation with a U-Net-like architecture
Author: [fchollet](https://twitter.com/fchollet)
Date created: 2019/03/20
Last modified: 2020/04/20
Description: Image segmentation model trained from scratch on the Oxford Pets dataset.
"""
"""
## Download the data
"""

"""shell
curl -O https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
curl -O https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
tar -xf images.tar.gz
tar -xf annotations.tar.gz
"""

"""
## Prepare paths of input images and target segmentation masks
"""

import tensorflow as tf
from tensorflow.python.keras import backend as K

# adjust values to your needs
config = tf.compat.v1.ConfigProto( device_count = {'GPU': 1 , 'CPU': 8} )
sess = tf.compat.v1.Session(config=config) 
K.set_session(sess)

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())


import os
import sys
import tensorflow as tf

input_dir = "images/"
target_dir = "annotations/trimaps/"
# img_size = (160, 160)
img_size = (128, 128)
num_classes = 3
batch_size = 32

input_img_paths = sorted(
    [
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
        if fname.endswith(".jpg")
    ]
)
target_img_paths = sorted(
    [
        os.path.join(target_dir, fname)
        for fname in os.listdir(target_dir)
        if fname.endswith(".png") and not fname.startswith(".")
    ]
)

print("Number of samples:", len(input_img_paths))

for input_path, target_path in zip(input_img_paths[:10], target_img_paths[:10]):
    print(input_path, "|", target_path)

"""
## What does one input image and corresponding segmentation mask look like?
"""

from IPython.display import Image, display
from tensorflow.keras.preprocessing.image import load_img
import PIL
from PIL import ImageOps

# Display input image #7
display(Image(filename=input_img_paths[9]))

# Display auto-contrast version of corresponding target (per-pixel categories)
img = PIL.ImageOps.autocontrast(load_img(target_img_paths[9]))
display(img)

# sys.exit()




"""
## Prepare `Sequence` class to load & vectorize batches of data
"""

from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import load_img


class OxfordPets(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            y[j] -= 1
        return x, y

class OxfordPetsMod(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
        r = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="float32")
        g = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="float32")
        b = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="float32")
        y = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_target_img_paths):
            # img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            # y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            # y[j] -= 1
            img = load_img(path, target_size=self.img_size)
            y[j] = img
            r[j] = np.expand_dims(y[j][:,:,0], 2)
            g[j] = np.expand_dims(y[j][:,:,1], 2)  
            b[j] = np.expand_dims(y[j][:,:,2], 2)  
        return x, r, g, b

class OxfordPetsMod1(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="uint8")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
            # x[j]=x[j]/255.0
        r = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        g = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        b = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        y = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            # img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            # y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            # y[j] -= 1
            img = load_img(path, target_size=self.img_size)
            y[j] = img
            # y[j] = y[j]/255.0
            r[j] = np.expand_dims(y[j][:,:,0], 2)
            g[j] = np.expand_dims(y[j][:,:,1], 2)  
            b[j] = np.expand_dims(y[j][:,:,2], 2)  
        return x, r#, g, b
    
class OxfordPetsMod2(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="uint8")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
            # x[j]=x[j]/255.0
        y = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            # img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            # y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            # y[j] -= 1
            img = load_img(path, target_size=self.img_size)
            y[j] = img
            # y[j] = y[j]/255.0
        return x, y
    
class OxfordPetsMod3():# it can not run with gpu
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = len(input_img_paths)-1#batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def getitem(self):
        batch_input_img_paths = self.input_img_paths[:]
        batch_target_img_paths = self.target_img_paths[:]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="uint8")
        # for j, path in enumerate(batch_input_img_paths):
        for j in range(len(batch_input_img_paths)-1):  
            path=batch_input_img_paths[j]
            img = load_img(path, target_size=self.img_size)
            x[j] = img
            # x[j]=x[j]/255.0
        y = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="uint8")
        # for j, path in enumerate(batch_target_img_paths):
        for j in range(len(batch_target_img_paths)-1):  
            path=batch_target_img_paths[j+1]
            # img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            # y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            # y[j] -= 1
            img = load_img(path, target_size=self.img_size)
            y[j] = img
            # y[j] = y[j]/255.0
        return x, y    

"""
## Prepare U-Net Xception-style model
"""

from tensorflow.keras import layers


def get_model(img_size, num_classes):
    inputs = keras.Input(shape=img_size + (3,))

    ### [First half of the network: downsampling inputs] ###

    # Entry block
    x = layers.Conv2D(32, 3, strides=2, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    # Blocks 1, 2, 3 are identical apart from the feature depth.
    for filters in [64, 128, 256]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(filters, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    ### [Second half of the network: upsampling inputs] ###

    for filters in [256, 128, 64, 32]:
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.UpSampling2D(2)(x)

        # Project residual
        residual = layers.UpSampling2D(2)(previous_block_activation)
        residual = layers.Conv2D(filters, 1, padding="same")(residual)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    # Add a per-pixel classification layer
    # outputs = layers.Conv2D(num_classes, 3, activation="softmax", padding="same")(x)
    outputs = layers.Conv2D(num_classes, 3, activation="linear", padding="same")(x)

    # Define the model
    model = keras.Model(inputs, outputs)
    return model

def get_model1_org(img_size, num_classes):
    inputs = keras.Input(shape=img_size + (3,))

    ### [First half of the network: downsampling inputs] ###

    # Entry block
    x = layers.Conv2D(32, 3, strides=2, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    # Blocks 1, 2, 3 are identical apart from the feature depth.
    for filters in [64, 128, 256]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(filters, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    ### [Second half of the network: upsampling inputs] ###

    for filters in [256, 128, 64, 32]:
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.UpSampling2D(2)(x)

        # Project residual
        residual = layers.UpSampling2D(2)(previous_block_activation)
        residual = layers.Conv2D(filters, 1, padding="same")(residual)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    # Add a per-pixel classification layer
    # outputs = layers.Conv2D(num_classes, 3, activation="softmax", padding="same")(x)
    outputs = layers.Conv2D(num_classes, 3, activation="linear", padding="same")(x)

    # Define the model
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model

def get_model1(img_size, num_classes):
    inputs = keras.Input(shape=img_size + (3,))

    ### [First half of the network: downsampling inputs] ###

    # Entry block
    x = layers.Conv2D(128, 3, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    # Blocks 1, 2, 3 are identical apart from the feature depth.
    for filters in [128]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        # x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(filters, 1, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    ### [Second half of the network: upsampling inputs] ###

    for filters in [128]:
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        # x = layers.UpSampling2D(2)(x)

        # Project residual
        # residual = layers.UpSampling2D(2)(previous_block_activation)
        residual = layers.Conv2D(filters, 1, padding="same")(previous_block_activation)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    # Add a per-pixel classification layer
    # outputs = layers.Conv2D(num_classes, 3, activation="softmax", padding="same")(x)
    outputs = layers.Conv2D(num_classes, 3, activation="linear", padding="same")(x)

    # Define the model
    model = keras.Model(inputs, outputs)
    return model


# Free up RAM in case the model definition cells were run multiple times
keras.backend.clear_session()


"""
## Set aside a validation split
"""

import random


# Split our img paths into a training and a validation set
val_samples = 1000
random.Random(1337).shuffle(input_img_paths)
random.Random(1337).shuffle(target_img_paths)
train_input_img_paths = input_img_paths[:-val_samples]
train_target_img_paths = target_img_paths[:-val_samples]
val_input_img_paths = input_img_paths[-val_samples:]
val_target_img_paths = target_img_paths[-val_samples:]

# Instantiate data Sequences for each split
# train_gen = OxfordPets(
#     batch_size, img_size, train_input_img_paths, train_target_img_paths
# )
train_gen = OxfordPetsMod3(
    batch_size, img_size, train_input_img_paths, train_input_img_paths
)
train_x,train_y=train_gen.getitem()


# val_gen = OxfordPets(batch_size, img_size, val_input_img_paths, val_target_img_paths)
val_gen = OxfordPetsMod3(batch_size, img_size, val_input_img_paths, val_input_img_paths)
val_x,val_y=val_gen.getitem()

img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_x[1]))
print(val_x[1].shape)
display(img1)
img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_y[1]))
print(val_y[1].shape)
display(img1)
img1=np.expand_dims(val_y[1][:,:,0], 2)
print(img1.shape)
img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(img1))
display(img1)
img1=np.expand_dims(val_y[1][:,:,1], 2)
print(img1.shape)
img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(img1))
display(img1)
img1=np.expand_dims(val_y[1][:,:,2], 2)
print(img1.shape)
img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(img1))
display(img1)

# sys.exit()



if os.path.exists('oxford_gen_color_r2_sht.h5') and os.path.isfile('oxford_gen_color_r2_sht.h5') :
    pass
    # load
    model=keras.models.load_model('oxford_gen_color_r2_sht.h5',compile=False)
    # model.summary()
    
    stringlist = []
    model.summary(print_fn=lambda x: stringlist.append(x))
    short_model_summary = "\n".join(stringlist)
    print(short_model_summary)
    fw = open("summary-oxford.txt", "w") 
    fw.write(str(short_model_summary))
    fw.close()
    
else :
    # Build model
    model = get_model1(img_size, num_classes)
    model.summary()
    
    stringlist = []
    model.summary(print_fn=lambda x: stringlist.append(x))
    short_model_summary = "\n".join(stringlist)
    # print(short_model_summary)
    fw = open("summary-oxford.txt", "w") 
    fw.write(str(short_model_summary))
    fw.close()
    
    """
    ## Train the model
    """

    # Configure the model for training.
    # We use the "sparse" version of categorical_crossentropy
    # because our target data is integers.
    # model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy")
    adam = tf.keras.optimizers.Adam()
    model.compile(optimizer=adam, loss="mae")
    
    callbacks = [
        keras.callbacks.ModelCheckpoint("oxford_gen_color_r2_sht.h5", save_best_only=True)
    ]
    
    # Train the model, doing validation at the end of each epoch.
    epochs = 15
    # model.fit(train_x,train_y, epochs=epochs, validation_data=(val_x,val_y), callbacks=callbacks)   
    model.fit(train_x,train_y, batch_size=1, epochs=epochs, validation_data=(val_x,val_y), callbacks=callbacks)   #batch_size=1 can run gpu
    pass

"""
## Visualize predictions
"""
# sys.exit()
# Generate predictions for all images in the validation set

# val_gen = OxfordPets(batch_size, img_size, val_input_img_paths, val_target_img_paths)
val_gen = OxfordPetsMod3(batch_size, img_size, val_input_img_paths, val_input_img_paths)
val_x,val_y=val_gen.getitem()

img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_x[1]))
print(val_x[1].shape)
display(img1)
img1.save('./out/oxford_gen_color_r2_sht_0.png')
img1 = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_y[1]))
print(val_y[1].shape)
display(img1)
img1.save('./out/oxford_gen_color_r2_sht_1.png')

val_preds = model.predict(val_x[1].reshape(1,val_x[1].shape[0], val_x[1].shape[1],val_x[1].shape[2]))
print(val_x[1].shape)
print(val_preds.shape)

def display_mask(i):
    """Quick utility to display a model's prediction."""
    img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_x[i]))
    display(img)
    img.save('./out/oxford_gen_color_r2_sht_2.png')
    
    img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_preds[0]))
    display(img)
    img.save('./out/oxford_gen_color_r2_sht_3.png')
    
    for j in range(val_preds.shape[-1]):
        img0 = np.expand_dims(val_preds[0][:,:,j], axis=-1)
        img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(img0))
        display(img)
        img.save('./out/oxford_gen_color_r2_sht_3_%d.png'%(j))



# Display results for validation image #10
i = 1

# Display input image
# display(Image(filename=val_input_img_paths[i]))

# Display ground-truth target mask
# img = PIL.ImageOps.autocontrast(load_img(val_target_img_paths[i]))
# display(img)

# Display mask predicted by our model
display_mask(i)  # Note that the model only sees inputs at 150x150.


# sys.exit()

img = PIL.ImageOps.autocontrast(load_img('./input/000004.jpg', target_size=img_size))
# img = PIL.ImageOps.autocontrast(load_img('./images/Abyssinian_1.jpg', target_size=(160, 160)))
# img = PIL.ImageOps.autocontrast(load_img('./annotations/trimaps/Abyssinian_1.png', target_size=(160, 160)))
display(img)
img.save('./out/oxford_gen_color_r2_sht_4.png')
x = np.zeros((1,)+img_size + (3,), dtype="uint8")
x[0]=img

val_preds = model.predict(x)
val_preds = (np.rint(val_preds)).astype(int)
print(x.shape)
print(val_preds.shape)

img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(val_preds[0]))
display(img)
img.save('./out/oxford_gen_color_r2_sht_5.png')

