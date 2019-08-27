import os
import json
import csv
# import uuid
import time
import random
import string
from os import path
from jinja2 import Environment
from jinja2 import FileSystemLoader
from werkzeug.exceptions import HTTPException, Forbidden
from werkzeug.exceptions import NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.urls import url_parse
from werkzeug.utils import redirect
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response
from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder


class Shortly(object):
    def __init__(self):
        self.url_map = Map([
            Rule('/', endpoint='index'),
            Rule('/search/', endpoint='search'),
            Rule('/savedata/', endpoint='save_data')
         ])
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
        loader=FileSystemLoader(template_path), autoescape=True)

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException as e:
            return e
  
    def index(self, request):
        sid = request.cookies.get('session_id')
        if sid is None:
            sid = random.randint(100,100000)
        id = str(sid)    
        sid = str(sid)

        data = []
        with open('contact.csv') as r:
            for row in r:
                data.append(row.split(","))
        del data[0]
        response = self.render_template('search.html', data=data)
        response.set_cookie('session_id',str(sid), expires=None, httponly=True)        
        return response

    def search(self, request):
        if request.cookies.get('session_id'):
            if request.method == "POST":
                csv_array = []
                data = request.form['txt_search_box']
                if data:
                    with open('contact.csv') as r:
                        x =  csv.reader(r)
                        for row in x:
                            if row[0] == data:
                                csv_array.append(row)          
                y = json.dumps(csv_array)
                return Response(y, mimetype="application/json")
            else:
                raise Forbidden()
        else:
             raise Forbidden()

    def save_data(self, request):
        session_id = request.cookies.get('session_id')
        if session_id:
            if request.method == "POST":
                data = request.form['row_val']
                name = request.form['name']
                if data.isnumeric():
                    data = "Mob. No"
                else:
                    data = "Email"
                with open('activity.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([session_id, name, data])
                return Response("Sucessfull", mimetype="application/text")
            else:
                raise Forbidden()
        else:
             raise Forbidden()        
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)     
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host="localhost", redis_port=6379, with_static=True):
    app = Shortly()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static'),
        })
    return app
 
if __name__ == "__main__":
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple("127.0.0.1", 8000, app, use_debugger=True, use_reloader=True)
