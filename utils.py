import pytz
import requests
import datetime

import app


def get_location(ip):
    url = f"https://freegeoip.app/json/{ip}"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_local_time(request):
    ip = request.headers.get('X-Forwarded-For', '127.0.0.1')
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
        'time': timestamp.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
        'year': timestamp.year,
        'month': timestamp.month,
        'day': timestamp.day,
        'hour': timestamp.hour,
        'minute': timestamp.minute,
        'second': timestamp.second,
        'tzname': timestamp.tzname(),
        'timezone': timestamp.tzinfo.zone,
        'delta': delta_str,
        'location': location.get('time_zone', 'UTC')
    }
    return context
