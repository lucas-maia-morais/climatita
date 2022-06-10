from operator import methodcaller
import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import aux

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        print(new_city)
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    cities = [city.name for city in cities]
    cities = list(dict.fromkeys(cities))

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2356b58400a9681ea05ad7545fae07e&units=metric'
    
    weather_data = []

    for city in cities:
        try:
            r = requests.get(url.format(city)).json()

            weather = {
                'city': r['name'],
                'temperature': int(float(r['main']['temp'])),
                'description': r['weather'][0]['description'],
                'dica': aux.dica(r['main']['temp']),
                'icon': r['weather'][0]['icon'],
            }
            weather_data.append(weather)
        except:
            pass


    return render_template('weather.html', weather_data = weather_data)