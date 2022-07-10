'''
To run this program, data files has to be downloaded from kaggle by "kaggle competitions download -c word2vec-nlp-tutorial" command and
unzipped to the directory named as "data".
Trained model has accuracy something like 0.89.
'''
import pandas as pd
import numpy as np
import tensorflow as tf
import re
import string
import matplotlib.pyplot as plt

from tensorflow.strings import lower
from tensorflow.strings import regex_replace
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.callbacks import EarlyStopping

# Read data and preview
train = pd.read_table("data/labeledTrainData.tsv")
print(train.head())

x_train = train.pop("review")
y_train = train.pop("sentiment")

print(x_train.head())
print(y_train.head())

x_train = np.asarray(x_train)
y_train = np.asarray(y_train)

def standardization(data):
    lowercase = lower(data)
    strippedhtml = regex_replace(lowercase, '<br />', ' ')
    return regex_replace(strippedhtml, '[%s]' % re.escape(string.punctuation), '')

# Build model

vectorize_layer = TextVectorization(
        standardize=standardization,
        max_tokens=15000,
        output_mode='int',
        output_sequence_length=500
        )

vectorize_layer.adapt(x_train)

model = Sequential([
    vectorize_layer,
    Embedding(15000, 16),
    GlobalAveragePooling1D(),
    Dense(64, activation="relu"),
    Dense(1, activation="sigmoid")
    ])

model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
        )

callbacks = [
        EarlyStopping(patience=2)
        ]

history = model.fit(
        x_train,
        y_train,
        validation_split=0.2,
        callbacks=callbacks,
        epochs=10
        )

# Plot results

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('accuracy')
plt.ylabel('acc')
plt.xlabel('epoch')
plt.legend(['train','val'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('los')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','val'], loc='upper left')
plt.show()
