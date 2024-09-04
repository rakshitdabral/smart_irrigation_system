import uvicorn
from fastapi import FastAPI
from Irrigation import Irrigation
import numpy as np
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = FastAPI()
pickle_in = open("classifier.pkl","rb")
classifier=pickle.load(pickle_in)


@app.get('/')
def index():
    return {'message': 'Hello, World'}


@app.post('/predict')
def predict_irrigation(data:Irrigation):
    data = data.dict()
    soil_moisture=data['SoilMoisture']
    temp=data['Temperature']
    soil_humidity=data['SoilHumidity']
    
    scaler = StandardScaler()
    input_data = (soil_moisture,temp,soil_humidity)
    input_data_as_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_array.reshape(1,-1)
    scaled_data = scaler.fit_transform(input_data_reshaped)
    std_data = scaler.transform(scaled_data)
    prediction = classifier.predict(std_data)
    if(prediction[0]>0.5):
        prediction="water the plant"
    else:
        prediction="donot water the plant"
    return {
        'prediction': prediction
    }

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload

