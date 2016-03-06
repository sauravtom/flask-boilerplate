#!/usr/bin/env python

import flask, flask.views
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
import json
import os
import json
import requests

from app import app




@app.route('/')
def home():
    return flask.render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')



