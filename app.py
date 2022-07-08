from crypt import methods
from email import message
from hmac import trans_36
from operator import methodcaller
from urllib import response
from googletrans import Translator
import requests
from flask import Flask, render_template, request, jsonify, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import aux

# Start app
app = Flask(__name__)
app.config['DEBUG'] = True
translator = Translator()

# Connect db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2356b58400a9681ea05ad7545fae07e&units=metric'

    if request.method == 'POST':
        try:
            new_city = request.form.get('city')
            r = requests.get(url.format(new_city)).json()

            exists = City.query.filter_by(name=r['name']).first()

            if exists is None:
                new_city_obj = City(name=r['name'])
                db.session.add(new_city_obj)
                db.session.commit()
        except:
            pass

    cities = City.query.all()
    cities = [city.name for city in cities]
    cities = list(dict.fromkeys(cities))

    weather_data = []

    for city in cities:
        try:
            r = requests.get(url.format(city)).json()

            weather = {
                'city': r['name'],
                'temperature': int(float(r['main']['temp'])),
                'description': translator.translate(r['weather'][0]['description'], src='en', dest='pt').text,
                'dica': aux.dica(r['main']['temp']),
                'icon': r['weather'][0]['icon'],
                'country': r['sys']['country'],
                'dt': r['dt'],
            }
            weather_data.append(weather)
        except:
            pass


    return render_template('weather.html', weather_data = weather_data)

@app.route('/<city_name>/delete_city', methods=['POST'])
def delete_city(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2356b58400a9681ea05ad7545fae07e&units=metric'
    try:
        r = requests.get(url.format(city_name)).json()

        cities = City.query.filter_by(name=r['name'])

        for city in cities:
            db.session.delete(city)
        db.session.commit()

        flash("City Deleted")
    except:
        pass

    return redirect(url_for('index'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    try:
        cities = City.query.all()
        for city in cities:
            db.session.delete(city)

        db.session.commit()
    except:
        pass
    
    return redirect(url_for('index'))


@app.route('/cities_weather', methods=['GET','POST'])
def all_cities_weather():
    response_object = {'status': 'success'}

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2356b58400a9681ea05ad7545fae07e&units=metric'
    
    if request.method == 'POST':
        try:
            new_city = request.get_json()
            r = requests.get(url.format(new_city['city'])).json()
            exists = City.query.filter_by(name=r['name']).first()

            if exists is None:
                new_city_obj = City(name=r['name'])
                db.session.add(new_city_obj)
                db.session.commit()
                response_object['message'] = 'Cidade Adicionada!'
            else:
                response_object['message'] = 'Cidade ja foi adicionada anteriormente!'
        except:
            response_object['message'] = 'Erro na adicao! Tente mais tarde.'
            response_object['status'] = 'failed'
    else:
        weather_data = []
        cities = City.query.all()
        # print(cities)
        # cities = [city.name for city in cities]
        # print(cities)
        # cities = list(dict.fromkeys(cities))
        # print(cities)

        for city in cities:
            # try:
                name = city.name
                r = requests.get(url.format(name)).json()

                description_en = r['weather'][0]['description']
                description_pt = translator.translate(description_en, src='en', dest='pt').text
                weather = {
                    'city_id': city.id,
                    'city': r['name'],
                    'temperature': int(float(r['main']['temp'])),
                    'description': description_pt,
                    'dica': aux.dica(r['main']['temp']),
                    'icon': r['weather'][0]['icon'],
                    'country': r['sys']['country'],
                    'dt': r['dt'],
                }
                weather_data.append(weather)
            # except:
            #     pass
        
        response_object['cities_weather'] = weather_data

    return jsonify(response_object)

@app.route('/cities_weather/<city_id>', methods=['PUT','DELETE'])
def single_city(city_id):
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2356b58400a9681ea05ad7545fae07e&units=metric'
    response_object = {'status': 'success'}
    old_city_obj = City.query.filter_by(id=city_id).first()

    if request.method == 'PUT':
        post_data = request.get_json()
        
        update_city = post_data.get('city')
        r = requests.get(url.format(update_city)).json()

        if old_city_obj.name == r['name']:
            response_object['message'] = 'Cidade é a mesma!'
        else:
            try:
                new_city_obj = City(name=r['name'])
                db.session.delete(old_city_obj)
                db.session.add(new_city_obj)
                db.session.commit()
                response_object['message'] = 'Cidade Atualizada!'
            except:
                response_object['message'] = 'Erro na atualização! Tente mais tarde'

    if request.method == 'DELETE':        
        try:
            db.session.delete(old_city_obj)
            db.session.commit()
            response_object['message'] = 'Cidade Deletada!'
        except:
            response_object['message'] = 'Erro na deleção! Tente mais tarde'

    return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run()