from flask import Flask, request,jsonify
from flask_mysqldb import MySQL

app = Flask(_name_)

@app.route('/')
def index():
    titulo = 'ievn-1001'
    list=['pedro', 'maria', 'jose']
    return reader_template('uno.html', titulo=titulo, list=list)
#@app.route('/user/<string:user>')

if _name_ == '_main_':
    app.run(debug=True)