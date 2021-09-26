db: odd_number
collection: number_pool
schema: 
{
  _id:
  number:
  searched:
  claimed: {
    datetime:
    message:
    veto:
  }
  records: [
    {
      datetime:
      selection:
      message:
      upvote:
      downvote:
    }
    ...
  ]
}


collection: ip_pool
schema:
{
  _id:
  ip:
  records: [
    datetime
    ...
  ]
  votes: {
    {
      datetime:
      vote-type:
    }
    ...
  }
}


possible abuse pattern and anti-abuse strategy:

G - good-willed user
B- ill-willed user
assuming G is at least 100x of B in quantity

1) B can post fake message saying a scam number is safe
- G can downvote the fake message

2) B can downvote G's helpful message
- every ip can only make one vote on one message

3) B can post many fake messages on one number
- every ip can post mostly 3 messages per day

4) B can claim to be the owner of one number and allege it is safe, or claim G's number
- G can veto the claim. If disapproval is more than 20, the claim will be removed from database

5) B can use VPN to change ip
- well, there is no solution if they go that extreme to abuse the system


things to note in frontend/backend design:
- due to the anti-abuse implementation, user might try to to create multiple messages or make many votes per day, 
need to reduce the backend/database query in that case