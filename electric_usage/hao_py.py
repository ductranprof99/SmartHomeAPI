import pandas as pd
from pathlib import Path
import numpy as np
from tensorflow.keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences

#################################
#     Tiền xử lý dữ liệu        #
#################################

data_dir = Path(__file__).absolute().parent
#import csv data file as a DataFrame panda type
with open(data_dir/'rawData.csv','rb') as f:
  df = pd.read_csv(f,  
            header=0, 
            names=[ 'NUM_MEM','RES_TYPE','INCOME','EDUCA','WK_STAT','HOURS'])
# Format input
format_data=[]
row=[]
for i in range(0,len(df.NUM_MEM)):
  row.append(df.NUM_MEM[i])
  row.append(df.RES_TYPE[i])
  row.append(df.INCOME[i])
  row.append(df.EDUCA[i])
  row.append(df.WK_STAT[i])
  format_data.append(row.copy())
  row.clear()

print(format_data[0:10])

#Transfer list to numpy array
data = pad_sequences(format_data, maxlen=5)
labels = np.array(df.HOURS)

#Random shuffle data
np.random.seed(10)
#Create new shuffle array index
indices = np.arange(data.shape[0])
np.random.shuffle(indices)

#apply above random index to our data
data = data[indices]
labels = labels[indices]

#Slice dataset to 2 component
training_samples = int(len(indices) * .8)
validation_samples = len(indices) - training_samples
X_train = data[:training_samples]
y_train = labels[:training_samples]
X_valid = data[training_samples:]
y_valid = labels[training_samples: ]
#################################
#     Trainning                 #
#################################
num = 20
embedding_dim = 20
# Create num*20 matrix
embedding_matrix = np.random.rand(num, embedding_dim)

from keras.models import Sequential
from keras.layers import Embedding,  Dense, LSTM
units =20
model = Sequential()
#Tạo 1 mô hình RNN lớp 1 là embedding lớp 2 là LSTM lớp 3 là hàm dense với hàm kích hoạt là  ReLU
model.add(Embedding(num, embedding_dim))
model.add(LSTM(units))
model.add(Dense(1, activation='ReLU'))

model.layers[0].set_weights([embedding_matrix])
# Khởi tạo trọng số
model.layers[0].trainable = True

#Setup the model
model.compile(optimizer="SGD",
              loss="mse",
              metrics=['acc'])
#Tranning
history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=8,
                    validation_data=(X_valid, y_valid))
#Save model
model.save(data_dir/"model1.h5")


