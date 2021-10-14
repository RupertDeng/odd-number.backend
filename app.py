from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from datetime import datetime
from config import DB_CONN_STR, APP_API_KEY

app = Flask(__name__)
client = MongoClient(DB_CONN_STR)
db = client.odd_number
number_pool = db.number_pool
ip_pool = db.ip_pool


@app.route('/')
def index():
  return '<h1>Website under construction. Please visit later.</h1>'


@app.route('/search/<number>', methods=['GET'])
def search(number):
  record = number_pool.find_one_and_update(
    {'number': number},
    {'$inc': {'searched': 1}},
    upsert=True,
    return_document=ReturnDocument.AFTER
    )
  result = {
    'searched': record['searched'],
    'messages': record['messages'] if 'messages' in record else [],
  }
  response = make_response(jsonify(result), 200)
  return response


@app.route('/add-message/<number>', methods=['POST'])
def add_message(number):
  data = request.get_json()
  time_id = str(datetime.now()).replace(' ', '+')
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
  response = make_response('message added', 200)
  return response


@app.route('/delete-message/<number>/<message_id>', methods=['DELETE'])
def delete_message(number, message_id):
  number_pool.update_one(
    {'number': number},
    {'$pull': {'messages': {'time_id': message_id}}}
  )
  response = make_response('message deleted', 200)
  return response


def register_vote(number, message_id, vote_type, operation):
  incre = 1 if operation == 'vote' else -1
  if vote_type == 'up':
    number_pool.update_one(
      {'number': number, 'messages.time_id': message_id},
      {'$inc': {'messages.$.upvote': incre}}
    )
  else:
    number_pool.update_one(
      {'number': number, 'messages.time_id': message_id},
      {'$inc': {'messages.$.downvote': incre}}
    )

@app.route('/vote/<number>/<message_id>/<vote_type>', methods=['PATCH'])
def vote_message(number, message_id, vote_type):
  register_vote(number, message_id, vote_type, 'vote')
  response = make_response('vote marked', 200)
  return response

@app.route('/unvote/<number>/<message_id>/<vote_type>', methods=['PATCH'])
def unvote_message(number, message_id, vote_type):
  register_vote(number, message_id, vote_type, 'unvote')
  response = make_response('vote reverted', 200)
  return response

  

if __name__ == '__main__':
  app.run(debug=True)






