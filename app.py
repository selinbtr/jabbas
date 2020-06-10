from flask import Flask, jsonify, render_template, send_from_directory, request
from flask_restful import reqparse
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard.html')

@app.route('/')
def index():
    return render_template('/dashboard.html')


@app.route('/endpoints')
def endpoints():
    return {'endpoints':['linear','linear100','base2']}   

@app.route('/charts')
def charts():
    return {'charts':['bar','line','doughnut']}   

@app.route('/welcome/<name>')
def welcome(name):
    return render_template('/welcome.html', name=name)


def getLength():
    length = request.args.get('length', None)
    if length:
        return min(int(length), 1000)
    else:
        return 10

@app.route('/linear')
def data1():
    length = getLength()
    return {'dataSetResults':[i for i in range(1, length+1)]}


@app.route('/linear100')
def data2():
    length = getLength()
    return {'dataSetResults':[100*i for i in range(1, length+1)]}

@app.route('/base2')
def data3():
    length = getLength()
    return {'dataSetResults':[2 ** i for i in range(1, length+1)]}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ =='__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=os.environ['PORT'])