from flask import Flask, render_template, request

from utils import get_local_time


app = Flask(__name__, template_folder='templates')


@app.route('/')
def time():
    context = get_local_time(request)
    return render_template('base.html', context=context)
