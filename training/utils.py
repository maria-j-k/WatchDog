from datetime import datetime
import requests

from .models import Weather
#from teams.models import Coordinates


api_key = 'fbbc6e682b82b0fc3538ae49dfa4621b'
url = 'https://api.openweathermap.org/data/2.5/weather?zip={},{}&lang={}&appid={}&units=metric'


def check_location(user):
    zip_code = user.zip_code
    country = user.country
    response = requests.get(url.format(zip_code, country, country, api_key))
    if response.json()['cod'] != 200:
        print(response.json())
        return None
    city = response.json()['name']
    offset = response.json()['timezone']
    something = response.json()['name']
    id_something = response.json()['id']
    lat = response.json()['coord']['lat']
    lon = response.json()['coord']['lon']
    coordinates = Coordinates.objects.create(city=city,
                            offset=offset,
                            something=something,
                            id_something=id_something,
                            lat=lat,
                            lon=lon)
    return coordinates


def check_weather(user):
    zip_code = user.zip_code
    country = user.country
    response = requests.get(url.format(zip_code, country, country, api_key))
    if response.json()['cod'] != 200:
        print(response.json())
        return None
    temp = response.json()['main']['temp']
    feels_like = response.json()['main']['feels_like']
    overall = response.json()['weather'][0]['description']
    pressure = response.json()['main']['pressure']
    humidity = response.json()['main']['humidity']
    wind = response.json()['wind']['speed']
    rise = response.json()['sys']['sunrise']
    sunrise = datetime.fromtimestamp(rise)
    print(f'sunrise: {sunrise}')
    sset = response.json()['sys']['sunset']
    sunset = datetime.fromtimestamp(sset)
    print(f'sunset: {sunset}')
    city = response.json()['name']
    offset = response.json()['timezone']

    weather = Weather.objects.create(temp=temp,
                        feels_like=feels_like,
                            overall=overall,
                            pressure=pressure,
                            humidity=humidity,
                            wind=wind,
                            sunrise=sunrise,
                            sunset=sunset,
                            location=city,
                            offset=offset)
    return weather

