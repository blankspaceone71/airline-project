from flask import Flask, render_template, request, jsonify
import util
import pymongo

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
        total_stops = int(request.form['t_s'])
        day_of_journey = int(request.form['day_j'])
        month_of_journey = int(request.form['month_j'])
        dep_hr = int(request.form['dep_hr'])
        dep_min = int(request.form['dep_min'])

        try:
            client = pymongo.MongoClient('mongodb+srv://abhiram0007:abhiram0007@cluster0.i7amj.mongodb.net/airlinedb')
            print(client)
            database_name = "airlinedb"
            _database = client[database_name]
            collection = 'airlinecollections'
            _collection = _database[collection]  ##collection
            x = _collection.find(
                {'airline': airline, 'source': source, 'destination': destination, 'additional_info': additional_info,
                 'total_stops': total_stops, 'day_of_journey': day_of_journey,
                 'month_of_journey': month_of_journey, 'dep_hr': dep_hr, 'dep_min': dep_min})
            maxx = set()
            m = {airline, source, destination, additional_info, total_stops, day_of_journey, month_of_journey, dep_hr,
                 dep_min}
            for i in x:
                for k, v in i.items():
                    maxx.add(v)

            if len(maxx) !=0:
                xy = maxx.symmetric_difference(m)
                z = list(xy)
                for i in z:
                    if type(i) == int:
                        #print(i)
                        reslt = 'Estimated Price ={}'.format(i)
                        return render_template('index.html', prediction=reslt)
            else:
                result = util.estimated_price(airline, source, destination, additional_info, total_stops,
                                              day_of_journey,
                                              month_of_journey, dep_hr, dep_min)

                my_dict = {'airline': airline, 'source': source, 'destination': destination,
                           'additional_info': additional_info, 'total_stops': total_stops,
                           'day_of_journey': day_of_journey, 'month_of_journey': month_of_journey, 'dep_hr': dep_hr,
                           'dep_min': dep_min, "Price": result}
                _collection.insert_one(my_dict)

                result1 = 'Estimated Price ={}'.format(result)

                return render_template('index.html', prediction=result1)

        except:
            return 'something is wrong'


if __name__ == "__main__":
    app.run()
