from tensorflow.keras.models import load_model
import  numpy as np
from pathlib import Path

def predictResult(numMem:int,resType:int,income:int,educa:int,wkStat:int):
    #keras model
    dir = Path(__file__).absolute().parent
    model = load_model(dir/'model1.h5')
    #Create input
    input=[numMem,resType,income,educa,wkStat]
    data = np.array([input])
    #Sử dụng biến pred này để so sánh
    pred= model.predict(data)[0]
    return pred