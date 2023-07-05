#  Flask Application for CRUD operations on MongoDB

## How to run the application locally
There are two ways of running the application locally
1. Using Docker 
2. Using normal python env

## Using docker
1. Make sure docker and docker compose is installed in your PC if not follow [this steps](https://docs.docker.com/engine/install/)
2. Clone the project in to your local machine
3. Run the following commands
```commandline
cd <project_location>
docker-compose build
docker-compose up -d
```
This will run your application in localhost:5000 with mongodb running in port 27017

## Using normal python env
1. Clone the git repo to your local 
2. Install virtualenvironment in your pc
3. Create a new virtual env
4. Create a .env file with following env vars MONGO_URI APP_HOST APP_PORT
5. Follow the commands
```commandline
cd <project_location>
pip install -r requirements.txt
flask run
```

Follow either of one your application should be running locally


## API Reference

#### Get all users

```http
  GET /users
```
returns all the users in the batch of 10

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `page`      | `int` | Optional defaultly we consider page as 1 |


#### Get a particular user

```http
  GET /users/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of the user to fetch details |

### Add a User

```http
  POST /users
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`     | `string` | **Required**. |
| `email`     | `string` | **Required**. and should be valid email id |
| `password`     | `string` | **Required**. and should be more than 6 chars long|


```http
  PUT /users/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`     | `string` | **Required**. else you will get validation error |


```http
  DELETE /users/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`     | `string` | **Required**. else you will get validation error |



## Screenshots
### Get all users
![Get all users](images/Get%20all%20users.png)

### Get user by ID
![Get user by id](images/Get%20user%20by%20ID.png)

### Add User
![Add user](images/Add%20user.png)

### Update user
![Update user by id](images/Update%20user%20by%20ID.png)

### Delete a user
![Delete a user by id](images/Delete%20a%20user.png)

## Additional information
1. In docker set up The mongo db is non-persistent When ever you start the application new db instance will be used
2. There a script called populate.py this is used to pre-populate the users data with faker library you can run this script to pre-populate 100 user data

### How to run populate.py script
```commandline
Run the docker-compose up -d 
do docker ps
get the container id of flask_assignment_app
do docker exec -it <container_id> bash
you will get inside the container
then run python populate.py it should populate 100 users data

```
