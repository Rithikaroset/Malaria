import joblib
import numpy as np
from flask import Flask,request, url_for, redirect, render_template

app = Flask(__name__)

model_DT = joblib.load('models/model_DT1.pkl')
model_GB = joblib.load('models/model_GB1.pkl')
model_KNN = joblib.load('models/model_KNN1.pkl')
model_LR = joblib.load('models/model_LR1.pkl')
model_RFC = joblib.load('models/model_RF1.pkl')
model_SVM = joblib.load('models/model_SVM1.pkl')

@app.route('/')
def hello_world():
    return render_template("MALARIAF.html")

@app.route('/predict',methods=['POST','GET'])
def predict():

    try:
        int_features=[int(x) for x in request.form.values()]
    except:
        return render_template('error.html')
    final=[np.array(int_features)]

    print(int_features)
    print(final)
    
    res_DT = model_DT.predict_proba(final)
    print('Predict Proba DT - {}'.format(res_DT))

    res_GB = model_GB.predict_proba(final)
    print('Predict Proba GB - {}'.format(res_GB))

    res_KNN = model_KNN.predict_proba(final)
    print('Predict Proba KNN - {}'.format(res_KNN))

    res_LR = model_LR.predict_proba(final)
    print('Predict Proba LR - {}'.format(res_LR))

    res_RFC = model_RFC.predict_proba(final)
    print('Predict Proba RFC - {}'.format(res_RFC))
 
    ensemble_result = [res_DT[0], res_GB[0], res_KNN[0], res_LR[0], res_RFC[0]]

    output = np.mean(ensemble_result, axis = 0)
    print(output)

    print('Final Prediction - Class {}'.format(output.argmax()))

    if output.argmax() == 1:
        return render_template('MALARIAF.html', pred='Danger.\nProbability of occuring is {}'.format(output[output.argmax()]))
    else:
        return render_template('MALARIAF.html', pred='Safe.\n Probability of occuring is {}'.format(output[output.argmax()]))

if __name__=='__main__':
    app.run(debug = True, threaded = True)
