from flask import Flask, render_template, request, send_from_directory

from utils import get_local_time, get_city_time

from logging.config import dictConfig
from tzwhere import tzwhere


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__, template_folder='templates', static_folder='static')

tz = tzwhere.tzwhere()


@app.route('/')
def time():
    context = get_local_time(request)
    return render_template('base.html', context=context)


@app.route('/<city>')
def city_time(city):
    context = get_city_time(city)
    return render_template('base.html', context=context)


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
