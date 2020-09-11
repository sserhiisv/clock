import pytz
import time
import requests
import datetime

import app

from geopy.geocoders import Nominatim


def get_location(ip):
    url = f"https://freegeoip.app/json/{ip}"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_local_time(request):
    forwarded = request.headers.get('X-Forwarded-For', '127.0.0.1')
    ip = forwarded.split(',')[0]
    if ip == '127.0.0.1':
        location = {'time_zone': 'UTC'}
    else:
        location = get_location(ip)
    time_zone = location.get('time_zone')
    app.app.logger.info(time_zone)
    app.app.logger.info(ip)
    if time_zone == '':
        time_zone = 'UTC'
    zone = pytz.timezone(time_zone)
    timestamp = datetime.datetime.now(zone)

    delta = timestamp.utcoffset().seconds // 3600
    delta_str = f'0{delta}:00' if delta < 10 else f'{delta}:00'
    context = {
        # 'time': timestamp.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
        # 'time': int(timestamp.strftime("%s")) * 1000,
        'time': timestamp.strftime('%a %b %d %Y %H:%M:%S'),
        'date': timestamp.strftime('%A, %d %B %Y'),
        'week': timestamp.strftime('%V'),
        'year': timestamp.year,
        'month': timestamp.month,
        'day': timestamp.day,
        'hour': timestamp.hour,
        'minute': timestamp.minute,
        'second': timestamp.second,
        'tzname': timestamp.tzname(),
        'unixtime': int(time.mktime(timestamp.timetuple())),
        'timezone': timestamp.tzinfo.zone,
        'delta': delta_str,
        'location': location.get('time_zone', 'UTC')
    }
    # import ipdb; ipdb.set_trace()
    return context


def get_city_time(city):
    success = True
    geolocator = Nominatim(user_agent="test")
    location = geolocator.geocode(city)

    if location:
        time_zone = app.tz.tzNameAt(location.latitude, location.longitude)
    else:
        time_zone = None

    if not time_zone:
        time_zone = 'UTC'
        success = False
    zone = pytz.timezone(time_zone)
    timestamp = datetime.datetime.now(zone)

    delta = timestamp.utcoffset().seconds // 3600
    delta_str = f'0{delta}:00' if delta < 10 else f'{delta}:00'
    context = {
        # 'time': int(timestamp.strftime("%s")) * 1000,
        # 'time': timestamp.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
        'time': timestamp.strftime('%a %b %d %Y %H:%M:%S'),
        'date': timestamp.strftime('%A, %d %B %Y'),
        'week': timestamp.strftime('%V'),
        'year': timestamp.year,
        'month': timestamp.month,
        'day': timestamp.day,
        'hour': timestamp.hour,
        'minute': timestamp.minute,
        'second': timestamp.second,
        'tzname': timestamp.tzname(),
        'timezone': timestamp.tzinfo.zone,
        'delta': delta_str,
        'location': time_zone,
        'address': location.address if location else 'UTC',
        'success': success
    }
    print(context)
    print(int(timestamp.strftime("%s")) * 1000, int(timestamp.strftime("%s")))
    # import ipdb; ipdb.set_trace()
    return context
