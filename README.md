# Flask-Verb-App

Flask-Verb-App is a Flask web application that provides endpoints for managing users and french verbs. It utilizes a MongoDB database for user and verb storage.

## API Endpoints

### Users

1. Create a User
   POST /v0/users/

- Request Body:

{
"email": "user@example.com",
"password": "password123",
"name": "John Doe"
}

- Response:

{
"id": "user_id"
}

2. User Login
   POST /v0/users/login

- Request Body:

{
"email": "user@example.com",
"password": "password123"
}

- Response:

{
"token": "user_token",
"expiration": 2592000,
"logged_user": {
"uid": "user_id",
"email": "user@example.com",
"name": "John Doe"
}
}

3. Fetch Users
   GET /v0/users/

- Request Header:
  x-access-token = "user_token"

- Response:
  {
  "users": [
  {
  "uid": "user_id",
  "email": "user@example.com",
  "name": "John Doe"
  },
  // ... other users
  ]
  }

### Verbs

1. Get a Single Verb
   GET /verbs/

- Request Header:
  x-access-token = "user_token"

- Request Body:
  {
  "verb": "example_verb"
  }

- Response:
  {
  "verb": {
  // ... verb details
  }
  }

2. Get a Random Verb
   GET /verbs/random/

- Request Header:
  x-access-token = "user_token"

- Request Body:
  {
  "quantity": 5
  }

- Response:
  {
  "verbs": [
  {
  // ... random verb details
  },
  // ... other random verbs
  ]
  }
  ... (Other Endpoints)

## Technologies Used:

- Python
- Flask Framework
- MongoDB
- JWT (JSON Web Tokens)
