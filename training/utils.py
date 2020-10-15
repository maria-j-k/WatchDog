from datetime import datetime
import requests

from .models import Weather
#from teams.models import Coordinates




def check_current(user):
    """ Checks current weather condition.
        Accepts: user object
        Returns: weather object
    """
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&lang={}&appid={}&units=metric'
    try:
        from watch_dog.local_settings import CURRENT_API_KEY
    except ModuleNotFoundError:
        print("Brak klucza api w pliku local_settings.py!")
        print("Uzupełnij dane i spróbuj ponownie!")
        exit(0)
    api_key = CURRENT_API_KEY
    lat = user.lat
    lon = user.lon
    exclude = 'minutely,hourly,daily,alerts'
    lang = user.country
    response = requests.get(url.format(lat, lon, exclude, lang, api_key))
    if response.status_code != 200:
        print(response.status_code)
        return None
    temp = response.json()['current']['temp']
    feels_like = response.json()['current']['feels_like']
    pressure = response.json()['current']['pressure']
    wind = response.json()['current']['wind_speed']
    overall = response.json()['current']['weather'][0]['description']
    weather = Weather.objects.create(temp=temp, feels_like=feels_like, overall=overall, pressure=pressure, wind=wind)
    return weather

def check_location(user):
    """Checks users location (latitude, longitude and city) and saves to user instance
    Accepts: user instance
    Returns: updated user instance"""
    url = 'https://api.openweathermap.org/data/2.5/weather?zip={},{}&lang={}&appid={}&units=metric'
    try:
        from watch_dog.local_settings import LOC_API_KEY
    except ModuleNotFoundError:
        print("Brak klucza api w pliku local_settings.py!")
        print("Uzupełnij dane i spróbuj ponownie!")
        exit(0)
    api_key = LOC_API_KEY
    zip_code = user.zip_code
    country = user.country
    response = requests.get(url.format(zip_code, country, country, api_key))
    if response.status_code != 200:
        print(response.json())
        return None
    user.lat = response.json()['coord']['lat']
    user.lon = response.json()['coord']['lon']
    user.offset = response.json()['timezone']
    user.location = response.json()['name']
    user.save()
#   coordinates = Coordinates.objects.create(city=city,
#                           offset=offset,
#                           something=something,
#                           id_something=id_something,
#                           lat=lat,
#                           lon=lon)
#   return coordinates
    return user


#def check_weather(user):
#    zip_code = user.zip_code
#    country = user.country
#    response = requests.get(url.format(zip_code, country, country, api_key))
#    if response.json()['cod'] != 200:
#        print(response.json())
#        return None
#    temp = response.json()['main']['temp']
#    feels_like = response.json()['main']['feels_like']
#    overall = response.json()['weather'][0]['description']
#    pressure = response.json()['main']['pressure']
#    humidity = response.json()['main']['humidity']
#    wind = response.json()['wind']['speed']
#    rise = response.json()['sys']['sunrise']
#    sunrise = datetime.fromtimestamp(rise)
#    print(f'sunrise: {sunrise}')
#    sset = response.json()['sys']['sunset']
#    sunset = datetime.fromtimestamp(sset)
#    print(f'sunset: {sunset}')
#    city = response.json()['name']
#    offset = response.json()['timezone']
#
#    weather = Weather.objects.create(temp=temp,
#                        feels_like=feels_like,
#                            overall=overall,
#                            pressure=pressure,
#                            humidity=humidity,
#                            wind=wind,
#                            sunrise=sunrise,
#                            sunset=sunset,
#                            location=city,
#                            offset=offset)
#    return weather
#
#def check_past_weather(user, when):
#    api_key = 'a16e03dd75ac6b1b99ab95a77dcc6d68'
#    url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&lang={}&appid={}&units=metric'
#    country = user.country
#    lat = user.lat
#    lon = user.lon
#    dt = when
#    weather_data = {}
#    response = requests.get(url.format(lat, lon, dt, country, api_key))
#    
#    if response.status_code != 200:
#        print(response.status_code)
#        return 
#    time_zone = response.json()['timezone']
#    print(f'time_zone: {time_zone}')
#    for item in response.json()['hourly']:
#        # print(datetime.fromtimestamp(item['dt']))
#        if abs(item['dt']-dt) <=1800:
#            weather_data['dt'] = datetime.fromtimestamp(item['dt'])
#            weather_data['temp'] = item['temp']
#            weather_data['feels_like'] = item['feels_like']
#            weather_data['pressure'] = item['pressure']
#            weather_data['wind_speed'] = item['wind_speed']
#            weather_data['description'] = item['weather'][0]['description']
#
#            print(weather_data)
#    
#    return weather_data



    # temp = response.json()['main']['temp']
    # feels_like = response.json()['main']['feels_like']
    # overall = response.json()['weather'][0]['description']
    # pressure = response.json()['main']['pressure']
    # humidity = response.json()['main']['humidity']
    # wind = response.json()['wind']['speed']
    # rise = response.json()['sys']['sunrise']
    # sunrise = datetime.fromtimestamp(rise)
    # print(f'sunrise: {sunrise}')
    # sset = response.json()['sys']['sunset']
    # sunset = datetime.fromtimestamp(sset)
    # print(f'sunset: {sunset}')
    # city = response.json()['name']
    # offset = response.json()['timezone']

    # weather = Weather.objects.create(temp=temp,
    #                     feels_like=feels_like, 
    #                     overall=overall, 
    #                     pressure=pressure, 
    #                     humidity=humidity, 
    #                     wind=wind, 
    #                     sunrise=sunrise, 
    #                     sunset=sunset, 
    #                     name=city, 
    #                     offset=offset)

    
