import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

app=Flask(__name__)

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    loaded_model = pickle.load(open(r"models/model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

# To tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result',methods = ['POST'])
def result():
    to_predict_list = request.form.to_dict()
    to_predict_list=list(to_predict_list.values())
    to_predict_list = list(map(int, to_predict_list))
    result = ValuePredictor(to_predict_list)
        
    return render_template("result.html", prediction=result)

if __name__ == "__main__":
	app.run(debug=True)