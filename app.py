from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import json
import util

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    # load_artifacts()


@app.route('/math', methods=['POST'])
def predict():
    if request.method == 'POST':
        airline = request.form['air_li']
        source = request.form['source']
        destination = request.form['destination']
        additional_info = request.form['add_inf']
        total_stops = request.form['t_s']
        day_of_journey = request.form['day_j']
        month_of_journey = request.form['month_j']
        dep_hr = request.form['dep_hr']
        dep_min = request.form['dep_min']

        result = util.estimated_price(airline, source, destination, additional_info, total_stops, day_of_journey,
                                      month_of_journey, dep_hr, dep_min)
        # result2=[airline, source, destination, additional_info, total_stops, day_of_journey,
        # month_of_journey, dep_hr, dep_min ,result]
# statement = 'Price ={}' \
                   # ',airline= {} ,source= {},destinantion= {},additional_info= {},total stops {},day of journey={},month ={},dep_hour={},dep_min={}'.format(
            #result, airline, source, destination, additional_info, total_stops, day_of_journey,
           # month_of_journey, dep_hr, dep_min, result)

    return render_template('index.html', prediction=result)


if __name__ == '__main__':
    util.load_artifacts()
    app.run(debug=True, port=5000)
    # load_artifacts()
