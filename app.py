from flask import Flask, render_template, request
import numpy as np
import pickle

# Flask app create
app = Flask(__name__)

# Trained model load karo
model = pickle.load(open('anemia_model.pkl', 'rb'))

@app.route('/')
def home():
    # index.html open karega
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Form se values read karo
    # Names EXACTLY same hone chahiye jaisa index.html me hain
    gender      = float(request.form['Gender'])
    hemoglobin  = float(request.form['Hemoglobin'])
    pcv         = float(request.form['PCV'])
    mcv         = float(request.form['MCV'])
    mchc        = float(request.form['MCHC'])

    # Features ko numpy array me convert karo (2D array)
    input_data = np.array([[gender, hemoglobin, pcv, mcv, mchc]])

    # Model se prediction
    prediction = model.predict(input_data)[0]

    # Message banao
    if prediction == 0:
        msg = "You don't have any Anemic Disease."
    else:
        msg = "You have anemic disease."

    # predict.html me message bhejo
    return render_template('predict.html', prediction_text=msg)

if __name__ == '__main__':
    app.run(debug=True)
