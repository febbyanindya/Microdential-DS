from flask import Flask, request, render_template
from keras.models import load_model
import numpy as np

app = Flask(__name__)

model = load_model('ann.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediksi')
def predict():
    return render_template('prediksi.html')

@app.route('/hasilprediksi', methods=['POST'])
def prediksi():
    pm10, so2, co, o3, no2 = [x for x in request.form.values()]

    data = []

    data.append(float(pm10))
    data.append(float(so2))
    data.append(float(co))
    data.append(float(o3))
    data.append(float(no2))
            
    predicted_bit = np.round(model.predict([data])).astype('int')
    prediction = [np.argmax(element) for element in predicted_bit]

    if prediction==[0]:
        hasil = 'SANGAT TIDAK SEHAT'
    elif prediction==[1]:
        hasil = 'TIDAK SEHAT'
    elif prediction==[2]:
        hasil = 'SEDANG'
    elif prediction==[3]:
        hasil = 'BAIK'

    return render_template('hasil.html', hasil_prediksi=hasil, pm10=pm10, so2=so2, co=co, o3=o3, no2=no2)

if __name__ == '__main__':
    app.run(debug=True)