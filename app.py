import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2356b58400a9681ea05ad7545fae07e&units=metric'
    city = 'São Paulo'

    r = requests.get(url.format(city)).json()
    print(r)

    weather = {
        'city': r['name'],
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }



    return render_template('weather.html', weather = weather)