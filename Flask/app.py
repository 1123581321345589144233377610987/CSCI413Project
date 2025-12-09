import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

app=Flask(__name__)

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,11)
    loaded_model = pickle.load(open(r"models/model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

# To tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result',methods = ['POST'])
@app.route('/result', methods=['POST'])
def result():
    form_data = request.form.to_dict()

    # Extract scalar inputs
    intensity = int(form_data["intensity"])
    carbs = int(form_data["carbs_g"])
    prot = int(form_data["prot_g"])
    fat = int(form_data["fat_g"])
    bolus = int(form_data["bolus_dose"]) if "bolus_dose" in form_data else 0
    basal = int(form_data["basal_dose"]) if "basal_dose" in form_data else 0
    is_asleep = int(form_data["is_asleep"])

    # One-hot encode time_of_day
    tod = form_data["time_of_day"]
    time_of_day_Morning = 1 if tod == "Morning" else 0
    time_of_day_Afternoon = 1 if tod == "Afternoon" else 0
    time_of_day_Evening = 1 if tod == "Evening" else 0
    time_of_day_Night = 1 if tod == "Night" else 0

    # Arrange features in the order expected by the model
    features = [
        intensity,
        carbs,
        prot,
        fat,
        bolus,
        basal,
        is_asleep,
        time_of_day_Afternoon,
        time_of_day_Evening,
        time_of_day_Morning,
        time_of_day_Night
    ]

    # Make prediction
    prediction = ValuePredictor(features)

    return render_template("result.html", prediction=prediction)

if __name__ == "__main__":
	app.run(debug=True)