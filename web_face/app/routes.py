from math import sin, cos, sqrt, atan2, radians

from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app.models import USERS, STATUS, BUFFER_PEOPLE, VISITED_PLACES
from app import app, db
from app.form import LoginForm, RegistrationForm

from loguru import logger

from test_plotly import create_map, create_graph
import pandas as pd
import plotly.express as px

import requests

import os
import sys

import json


def get_address(lon, lat):
    API_KEY = '5c6f743d-2033-4fb4-84d0-60941cb65cc2'

    URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={lat},{lon}&format=json"
    result = requests.get(URL).json()
    print(result)
    return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

def get_nearest(lat, lon, type):
    API_KEY = '5ff9b945-0f5c-4355-8c90-fe93681fea26'
    URL = f"https://search-maps.yandex.ru/v1/?text={type}&type=biz&lang=ru_RU&ll={lon}, {lat}&results=6&spn=0.009,0.016&rspn=1&format=json&apikey={API_KEY}"
    result = requests.get(URL).json()
    logger.debug(result)
    if result['properties']['ResponseMetaData']['SearchResponse']['found'] != 0:
        return result['features']
    else:
        return 'Not found'

def get_lat_lon(addres):
    API_KEY = '5c6f743d-2033-4fb4-84d0-60941cb65cc2'
    URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={addres}&format=json"
    result = requests.get(URL).json()
    logger.debug(result, result[0]['geometry']['coordinates'])
    return result[0]['geometry']['coordinates']

@app.route('/find_covid/')
@app.route('/find_covid/index', methods = ['GET', 'POST'])
@login_required
def index():
    logger.debug(request.get_data().decode('utf-8'))
    if request.method == 'POST':
        pass
             

    return render_template("base.html", type_of_route = 'index', navigation=['Статистика','Личный кабинет','Выход'])



# Логика регистрации на сайте(Не относится к API)
@app.route('/find_covid/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print('!@!!!!!!!!!!!!!!!!!!')
        user = USERS.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            print('ERROR')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login_1.html', title='Sign In', form=form)

@app.route('/find_covid/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/find_covid/account')
def LK():
    user_email = current_user.email
    user_id = current_user.id
    return render_template('LK.html', id=user_id, email=user_email, navigation=['Статистика','Личный кабинет','Выход'])


@app.route('/find_covid/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = USERS(name=form.name.data, email=form.email.data)
        status_info = STATUS(id=user.id, test_result=form.status.data, сontact_with_infected=form.contact.data, Symptoms=form.symptoms.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.add(status_info)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/find_covid/map', methods=['GET', 'POST'])
def map():
    ru_cities = pd.read_csv("ru.csv")
    map = create_map(ru_cities)
    graph_1 = create_graph([6060,11237,8536,6632,5204,5195,9412,20985],'Заражения каронавирусом')
    graph_2 = create_graph([40,58,94,104,70,51,107,256],'Смерть от коронавируса')
    return render_template('map.html', plot=map, graph_1 = graph_1, graph_2 = graph_2 ,type_of_route = 'map', navigation=['Статистика','Личный кабинет','Выход'])

# Логика отработки API(Не относится к сайту)

# Логика отправки текущей геолокации
@app.route('/find_covid/get_user_data', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        pharamacies = []
        json_data = request.get_json()
        user = USERS.query.filter_by(email=json_data['email']).first()
        user.add_geo(f"{json_data['lat']}|{json_data['lon']}")
        user_id = user.id
        status_info = STATUS.query.filter_by(id=user_id).first()
        lat = json_data['lat']
        lon = json_data['lon']
        print(lat,lon)
        geolocation = get_address(lat,lon)
        near_pharamacies = get_nearest(lat, lon, 'Аптеки')
        for item in near_pharamacies:
            print(item['geometry']['coordinates'])
            print(type(item['geometry']['coordinates']))
            pharamacies.append(item['geometry']['coordinates'])
        logger.debug(near_pharamacies)
        return jsonify({ 'user_data':{
            'name': geolocation,
            'name' : user.name,
            'status': status_info.test_result,
            'contact': status_info.сontact_with_infected,
            'symptoms': status_info.Symptoms,
            'geolocation': geolocation
            }, 'near_pharamacies':{
            'data':pharamacies,
            }
            
            })

@app.route('/find_covid/edit_user_data', methods=['GET', 'POST'])
def edit_user_data():
    if request.method == 'POST':
        json_data = request.get_json()
        logger.debug(json_data)
        user = USERS.query.filter_by(email=current_user.email).first()
        status_info = STATUS.query.filter_by(id=user.id).first()
        print(status_info)
        status_info.edit_test_result(json_data['status'])
        status_info.edit_сontact_with_infected(json_data['contact'])
        status_info.edit_symptoms(json_data['symptoms'])
        print(status_info)
    return 'ok'

@app.route('/find_covid/probability_of_infection', methods=['GET', 'POST'])
def probability_of_infection():
    if request.method == 'POST':
        count = 0
        json_data = request.get_json()
        bufer_people = BUFFER_PEOPLE.query.all()
        summ_geolocation = round(json_data['lat'] + json_data['lon'], 5)
        print(summ_geolocation)
        for position in bufer_people:
            print(float(position.geolocation))
            # print(abs(summ_geolocation - float(position.geolocation)))
            print(summ_geolocation - float(position.geolocation))
            if abs(summ_geolocation - float(position.geolocation)) <= 0.00004:
                count += 1
        if BUFFER_PEOPLE.query.filter_by(id = json_data['id']).first():
            bufer_people = BUFFER_PEOPLE.query.filter_by(id = json_data['id']).first()
            bufer_people.edit_geolocation(json_data['lat'] + json_data['lon'])
            bufer_people.edit_type_of_public(json_data['type_of_public'])
        else:
            bufer_people = BUFFER_PEOPLE(id = json_data['id'], geolocation = json_data['lat'] + json_data['lon'], type_of_public = json_data['type_of_public'])
            db.session.add(bufer_people)
            db.session.commit()
        if count <= 2:
            return '5%'
        elif count <= 5:
            return '20%'
        else:
            return '60+%'
          
    return 'ok'

@app.route('/find_covid/chek_position', methods=['GET', 'POST'])
def chek_position():
    if request.method == 'POST':
        count = 0
        json_data = request.get_json()
        print(json_data)
        bufer_people = BUFFER_PEOPLE.query.all()
        lat = json_data['lat']
        lon = json_data['lon']
        addres = json_data['addres']
        print(addres)
        end_lat = get_lat_lon(addres)[0]
        end_lon = get_lat_lon(addres)[1]
        summ_geolocation = round(end_lat + end_lon, 5)
        for position in bufer_people:
            print(float(position.geolocation))
            # print(abs(summ_geolocation - float(position.geolocation)))
            print(summ_geolocation - float(position.geolocation))
            if abs(summ_geolocation - float(position.geolocation)) <= 0.00004:
                count += 1
        if count >= 3:
            for item in get_nearest(end_lat, end_lon, json_data['type']):
                print(item['geometry']['coordinates'])
                print(type(item['geometry']['coordinates']))
                objected.append(item['geometry']['coordinates'])
            return objected
        else:
            return 'Normal'
          
    return 'ok'


@app.route('/find_covid/user_at_home', methods=['GET', 'POST'])
def user_at_home():
    json_data = request.get_json()
    bufer_people = BUFFER_PEOPLE.query.filter_by(id=json_data['id']).first()
    db.session.delete(bufer_people)
    db.session.commit()
    return 'ok'

@app.route('/find_covid/add_visited_places', methods=['GET', 'POST'])
def visited_places():
    json_data = request.get_json()
    visited_places = VISITED_PLACES(user_id=json_data['user_id'], lat=json_data['lat'], lon=json_data['lon'], type_of_public=json_data['type_of_public'])
    db.session.add(visited_places)
    db.session.commit()
    return 'ok'


@app.route('/find_covid/route_to_the_pharmacy', methods=['GET', 'POST'])
def route_to_the_pharmacy():
    json_data = request.get_json()
    lat = json_data['lat']
    lon = json_data['lon']
    near_pharamacies = get_nearest(lat, lon)
    for item in near_pharamacies:
        print(near_pharamacies[0]['geometry']['coordinates'])
    return 'ok'

# Подсчёт кратчайшего расстояния между двумя точками
# @app.route('/get_shortest_distance', methods=['GET', 'POST'])
# def location():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         user1 = USERS.query.filter_by(email=json_data['email1']).first()
#         user_id1 = user.id
#         status1_info = STATUS.query.filter_by(id=user_id1).first()
#         user1 = USERS.query.filter_by(email=json_data['email1']).first()
#         user_id1 = user.id
#         status1_info = STATUS.query.filter_by(id=user_id1).first()
#         lat1 = json_data['lat1']
#         lon1 = json_data['lon1']
#         # approximate radius of earth in km
#         R = 6373.0

#         lat1 = radians(52.2296756)
#         lon1 = radians(21.0122287)
#         lat2 = radians(52.406374)
#         lon2 = radians(16.9251681)

#         dlon = lon2 - lon1
#         dlat = lat2 - lat1

#         a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))

#         distance = R * c

#         print("Result:", distance)
#         print("Should be:", 278.546, "km")



