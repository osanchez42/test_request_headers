from flask import Flask
from flask import request
import datetime

app = Flask(__name__)

"""
TO RUN:
1. copy and overwrite contents of nginx.conf to /etc/nginx/nginx.conf

2. move to project directory and run the following command (single line)

uwsgi --http :8000 -s /tmp/test_request_headers.sock --manage-script-name 
--mount /test_request_headers=app:app 
virtualenv ~/PycharmProjects/test_request_headers/venv/

3. opened port 8000 with ngrok

4. go to generated ngrok url and done. logs will me written to flask_uwsgi.log file in the root directory

"""


@app.route('/')
def hello_world():

    try:
        if request.method == "GET":
            page = 'Received GET request<br>' \
                'Request Object type: ' + str(type(request)) + '<br><br>'\
                'Request headers contained the following items:<br><br>' \
                '%s' % stylized_headers(request.headers)
            write_to_log(page)
            return page
        elif request.method == "POST":
            page = 'Received POST request<br>' \
                'Request Object type: ' + str(type(request)) + '<br><br>'\
                'Request headers contained the following items<br><br>' \
                '%s' % stylized_headers(request.headers)
            write_to_log(page)
            return page
    except Exception as e:
        write_to_log(e.message)
        return 'encountered an error'


def stylized_headers(request_headers):
    header_text = ''
    try:
        for key in request_headers.keys():
            value = request_headers.get(key)
            header_text += str(key) + ': ' + str(value) + '<br>'
    except Exception as e:
        header_text = e.message

    return header_text


def write_to_log(message):
    try:
        f = open('flask_uwsgi.log', "w")
        current_time = datetime.datetime.now()
        f.write('[Server]:  ' + str(current_time) + ': ' + str(message))
        f.close()
    except Exception:
        print 'error encountered'


if __name__ == '__main__':
    app.run()
