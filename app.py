from flask import Flask, request, make_response
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from datetime import datetime
from pytz import timezone, utc
from config import DB_CONN_STR, APP_API_KEY, FE_STR
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': FE_STR}})
client = MongoClient(DB_CONN_STR)
db = client.odd_number
number_pool = db.number_pool


@app.route('/')
def index():
  return '<h1>Please visit the web app <a href="https://odd-number.netlify.app/">"Odd Number"</a> for full service.</h1>'


# endpoint for seraching a number
@app.route('/search/<number>', methods=['GET'])
def search(number):
  # check API Key authentication
  auth = request.headers.get('X-Api-Key')
  if auth != APP_API_KEY:
    return make_response('API access not granted', 401)

  # query database and return result
  record = number_pool.find_one_and_update(
    {'number': number},
    {'$inc': {'searched': 1}},
    upsert=True,
    return_document=ReturnDocument.AFTER
    )
  result = {
    'number': record['number'],
    'searched': record['searched'],
    'messages': record['messages'] if 'messages' in record else [],
  }
  response = make_response(result, 200)
  return response

# endpoint to add a message under a number
@app.route('/add-message/<number>', methods=['POST'])
def add_message(number):
  # check API Key authentication
  auth = request.headers.get('X-Api-Key')
  if auth != APP_API_KEY:
    return make_response('Api access not granted', 401)

  # get visitorId from cookie to assign as message owner. if no cookie, assign one.
  visitorId = request.cookies.get('visitorId')
  if not visitorId:
    vID = uuid4().hex
  else:
    vID = visitorId

  # update database with the new message
  data = request.get_json()
  time_id = str(datetime.now(tz=utc).astimezone(timezone('US/Eastern'))).replace(' ', '~')
  new_message = {
      'vID': vID,
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
  response = make_response(new_message, 200)
  if not visitorId:
    response.set_cookie('visitorId', vID)
  return response

# endpoint to delete a specific message under a number
@app.route('/delete-message/<number>/<message_id>', methods=['DELETE'])
def delete_message(number, message_id):
  # check API Key authentication
  auth = request.headers.get('X-Api-Key')
  if auth != APP_API_KEY:
    return make_response('Api access not granted', 401)

  # get visitorId from cookie and check against database message owner. reject request if not match
  visitorId = request.cookies.get('visitorId')
  message_posted = number_pool.find_one({'number': number, 'messages.time_id': message_id}, {'messages.vID.$': 1})
  message_owner = message_posted['messages'][0]['vID']
  if visitorId != message_owner:
    return make_response('Operation not allowed', 405)
  
  # update database to delete the message
  number_pool.update_one(
    {'number': number},
    {'$pull': {'messages': {'time_id': message_id}}}
  )
  response = make_response(f'message {message_id} deleted', 200)
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

# endpoint to vote on a specific message under a number
@app.route('/vote/<number>/<message_id>/<vote_type>', methods=['PATCH'])
def vote_message(number, message_id, vote_type):
  auth = request.headers.get('X-Api-Key')
  if auth != APP_API_KEY:
    return make_response('Api access not granted', 401)
  register_vote(number, message_id, vote_type, 'vote')
  response = make_response('vote marked', 200)
  return response

# endpoint to unvote on a specifc message under a number
@app.route('/unvote/<number>/<message_id>/<vote_type>', methods=['PATCH'])
def unvote_message(number, message_id, vote_type):
  auth = request.headers.get('X-Api-Key')
  if auth != APP_API_KEY:
    return make_response('Api access not granted', 401)
  register_vote(number, message_id, vote_type, 'unvote')
  response = make_response('vote reverted', 200)
  return response

  

if __name__ == '__main__':
  app.run(debug=True)






