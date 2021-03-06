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
import hashlib
from app import app

from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "john": "hello",
    "foo": "food"
    }

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d

def spreadsheet_query():
    url = "https://spreadsheets.google.com/feeds/list/1rOvWwcvrKj_aNy4PVGNdUZdPC49d4zE6ncu0nGeN1Xw/od6/public/values?alt=json"
    #url = "https://spreadsheets.google.com/feeds/list/11f8Nr-FehZDT7j-tK_tQSf2bNkwZmNpRQa55-6wYeRg/od6/public/values?alt=json"
    json_ob = requests.get(url).json()
    arr = []
    for i in json_ob["feed"]["entry"]:
        d= {}
        title = i["gsx$title"]["$t"]
        image_url = i["gsx$imageurl"]["$t"]
        link = i["gsx$link"]["$t"]
        summary = i["gsx$summary"]["$t"]
        news_id = hashlib.md5(title+link).hexdigest()[:6]
        d = get_dict(news_id=news_id,link=link,image_url=image_url,summary=summary,title=title)
        arr.append(d)
    return arr

@app.route('/')
def home():
    arr = spreadsheet_query()
    return flask.render_template('index.html',arr=arr)

@app.route('/news/<news_id>')
def newsPage(news_id):
    arr = spreadsheet_query()
    news_data = None
    
    #news_data = [news for news in arr where news['news_id'] == news_id]

    for news in arr:
        if news['news_id'] == news_id:
            news_data = news

    if not news_data:
        return flask.render_template('404.html')
    else:
        return flask.render_template('news.html',news_data=news_data)


@app.route('/admin')
@auth.login_required
def admin():
    return flask.render_template('admin.html')

@app.route('/api')
def api():
    data = spreadsheet_query()
    return jsonify(arr=data)

@app.route('/api/<word>')
def apis(word):
    data = spreadsheet_query()
    searched_data = [news for news in data if word in news['summary']]
    return jsonify(arr=searched_data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')



