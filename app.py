from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.odd_number
number_pool = db.number_pool
ip_pool = db.ip_pool

@app.route('/')
def index():
  return '<h1>Website under construction. Please visit later.</h1>'

@app.route('/search/<number>')
def search(number):
  








