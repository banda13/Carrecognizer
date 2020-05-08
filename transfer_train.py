from PIL import ImageFile
from keras import Sequential, Model
from keras.applications import MobileNetV2
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint, History
from keras.layers import Dense, Flatten, Dropout, GlobalAveragePooling2D
from keras.optimizers import RMSprop
from keras.regularizers import l2
from keras_preprocessing.image import ImageDataGenerator

import numpy as np
import matplotlib.pyplot as plt

from classifiers.lstm0 import NameGenerator

train_dir = "data/train/"
validation_dir = "data/validation/"

image_size = 160  # All images will be resized to 160x160
batch_size = 16

unique_name = NameGenerator().get_name()


def batch_generator(X_gen, Y_gen):
    while True:
        yield (X_gen.next(), Y_gen.next())


ImageFile.LOAD_TRUNCATED_IMAGES = True

# Rescale all images by 1./255 and apply image augmentation
train_datagen = ImageDataGenerator(
    shear_range=0.2,
    zoom_range=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rescale=1. / 255)

validation_datagen = ImageDataGenerator(rescale=1. / 255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode='categorical')

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,  # Source directory for the validation images
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode='categorical')

np.save(("%s_class_indices.npy" % unique_name), train_generator.class_indices)

IMG_SHAPE = (image_size, image_size, 3)
num_classes = len(train_generator.class_indices)

# Create the base model from the pre-trained model MobileNet V2
base_model = MobileNetV2(input_shape=IMG_SHAPE,
                         include_top=False,
                         weights='imagenet')
base_model.trainable = False

top_model = Sequential()
top_model.add(GlobalAveragePooling2D())
top_model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
top_model.add(Dropout(0.5))
top_model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
top_model.add(Dropout(0.5))
top_model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
top_model.add(Dropout(0.5))
top_model.add(Dense(num_classes, activation='softmax', kernel_regularizer=l2(0.01)))
model = Model(input=base_model.input, output=top_model(base_model.output))
model.compile(optimizer=RMSprop(lr=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
# model.summary()

epochs = 100
steps_per_epoch = train_generator.n // batch_size
validation_steps = validation_generator.n // batch_size

callbacks = [EarlyStopping(monitor='val_loss',
                           min_delta=0,
                           patience=3,
                           verbose=0, mode='auto'),
             ModelCheckpoint(filepath=("%s-model-weights.h5" % unique_name), verbose=1, save_best_only=True),
             History(),
             TensorBoard(log_dir="logs/{}".format(unique_name))]

try:
    model.load_weights(("%s-model-weights.h5" % unique_name))
except OSError:
    pass

history = model.fit_generator(train_generator,
                              steps_per_epoch=steps_per_epoch,
                              epochs=epochs,
                              workers=4,
                              callbacks=callbacks,
                              validation_data=validation_generator,
                              validation_steps=validation_steps)

acc = history.history['acc']
val_acc = history.history['val_acc']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()), 1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0, max(plt.ylim())])
plt.title('Training and Validation Loss')
plt.savefig("%s-transfertrain.png" % unique_name)
plt.close()

base_model.trainable = True

# Let's take a look to see how many layers are in the base model
print("Number of layers in the base model: ", len(base_model.layers))

# Fine tune from this layer onwards
fine_tune_at = 100

# Freeze all the layers before the `fine_tune_at` layer
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(lr=2e-5),
              metrics=['accuracy'])
# model.summary()

history_fine = model.fit_generator(train_generator,
                                   steps_per_epoch=steps_per_epoch,
                                   epochs=epochs,
                                   callbacks=callbacks,
                                   workers=4,
                                   validation_data=validation_generator,
                                   validation_steps=validation_steps)

model.save("new_model.h5")

acc += history_fine.history['acc']
val_acc += history_fine.history['val_acc']

loss += history_fine.history['loss']
val_loss += history_fine.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.ylim([0.9, 1])
plt.plot([epochs - 1, epochs - 1], plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.ylim([0, 0.2])
plt.plot([epochs - 1, epochs - 1], plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.savefig("%s-finetune.png" % unique_name)
plt.close()
