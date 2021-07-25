from keras.models import load_model
import  numpy as np
from pathlib import Path
#keras model
dir = Path(__file__).absolute().parent
model = load_model(dir/'model1.h5')
#Create input
input=[8,	18,	5,	3,	4]
data = np.array([input])
#Predict
print(data)
#Sử dụng biến pred này để so sánh
pred= model.predict(data)[0]
print(pred)