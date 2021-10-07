from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from datetime import datetime

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
  record = number_pool.find_one_and_update(
    {'number': number},
    {'$inc': {'searched': 1}},
    upsert=True,
    return_document=ReturnDocument.AFTER
    )
  response = {
    'searched': record['searched'],
    'messages': record['messages'] if 'messages' in record else [],
  }
  return jsonify({'response': response})


@app.route('/add-message/<number>', methods=['POST'])
def add_message(number):
  data = request.get_json()
  time_id = str(datetime.now())
  new_message = {
      'time_id': time_id,
      'tag': data['tag'],
      'text': data['text'],
      'upvote': 0,
      'downvote': 0
    }
  number_pool.update_one(
    {'number': number},
    {'$push': {'messages': new_message}},
    upsert=True
  )
  response = make_response('message added', 201)
  return response








if __name__ == '__main__':
  app.run(debug=True)






