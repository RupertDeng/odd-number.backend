from flask import Flask, jsonify
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
  number_pool.update_one(
    {'number': number},
    {'$inc': {'searched': 1}},
    upsert=True
    )
  record = number_pool.find_one({'number': number})
  response = {
    'searched': record['searched'],
    'messages': record['messages'] if 'messages' in record else [],
  }
  return jsonify({'response': response})






if __name__ == '__main__':
  app.run(debug=True)






