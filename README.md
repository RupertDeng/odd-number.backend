# Backend app for "Odd Number" web app
## An anonymous platform to help user idenfity un-familiar phone call number
<br/>

## Basic function of the web app:
- User can search for any U.S phone number.
- User who knows some info of any phone number can post message to inform others.
- User can like or dislike other's message to help highlight useful information.
<br/>

## Backend implementation details:
- Auto-deployed to `heroku` from github repository, configured with gunicorn server and gevent workers.
- Non-relational database with phone number as primary key hosted on `MongoDB Altas`.
- Restful API framework enabled by `flask`: GET - search, POST - post message, PATCH - like/dislike on message, DELETE - delete message.
- Since the frontend is not hosted on heroku, cross-origin access is managed by `flask-cors` and api key.
<br/>

## Simple backend rate limiter
- Since this is an anonymous web app, user could abuse the message posting and voting system, by posting malicious/misleading message and/or voting unhelpfully.
- A simple rate limiter is implemented on backend to mitigate this concern (although can't completely prevent it).
- The same ip address can only post at most 5 messages and vote at most 10 times in every 24 hours.
- Rate limiter data is stored in heroku `memcached cloud`.
<br/>

### _For frontend implementation, please check the repository: ['Odd Number' Frontend](https://github.com/RupertDeng/odd-number.frontend)_ 
