# MPB
## Setup

### The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/SeifAldenFarhan/MPB.git
$ cd MPB
```

### Create a virtualenv and install Django and any other requirements
In your Bash console, create a virtualenv, naming it after your project, and choosing the version of Python you want to use:
```sh
$ mkvirtualenv --python=/usr/bin/python3.8 env
(env)$ pip install django
(env)$ pip install -r requirements.txt
```

### Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.
### Once pip has finished downloading the dependencies:
```sh
(env)$ cd MPB
(env)$ python manage.py runserver
```

## About the project
First of all, the user needs to register to use the other functions.
Then, the user login by his/her username and password.
After the login, the user can see all the blogs, can write a new blog(post), and edit or delete it if and only if he/she is the author.
Also, the user can like the others' posts or unlike (if he/she like the posts already).
The user can share the other's posts.
In the end, the user can logout.

## The API
#### All the responses are JSON.
### The fields' name that expected to use are:
1. post_id - the post id that defined automatically in the database.
2. post_content - the post content when new blog posted.
3. new_content - the post content when user edit his/her exist post.
4. username - the username of a user when register or login.
5. password - the password of a user when register or login.
6. email - the email of a user when register.

### The API requests:
- 1 API to allow all users to see the posted blogs:
```sh
GET http://127.0.0.1:8000/posts/
```
- 2 APIs to allow all users to like posts.
```sh
url = http://127.0.0.1:8000/likepost/
body = {'post_id': 1}
headers = {} // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 2a Only the user that liked the post can remove his like.
```sh
url = http://127.0.0.1:8000/unlikepost/
body = {'post_id': 1}
headers = {} // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 3 APIs to allow some users to post blog posts.
```sh
url = http://127.0.0.1:8000/newpost/
body = {'post_content': 'Hi, I am a new post'}
headers = {} // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 3a1 Only the users that wrote/posted the blog post can edit
```sh
url = http://127.0.0.1:8000/editpost/
body = {'post_id': 1, 'new_content': 'new content'}
headers = {} // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 3a2 delete the post.
```sh
url = http://127.0.0.1:8000/deletepost/
body = {'post_id': 1}
headers = {} // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 4 Very basic user registration
```sh
url = http://127.0.0.1:8000/register/
body = {'username': 'Seif', 'email': 'seif@gmail.com', 'password': 'seif123'}
headers = {}
response = requests.request("POST", url, headers=headers, data=body)
```
- 5 Authentication should be based on Basic Auth for the registered users (Bonus for JWT)
```sh
url = http://127.0.0.1:8000/login/
body = {'username': 'Seif', 'password': 'seif123'}
headers = {}
response = requests.request("POST", url, headers=headers, data=body)
```
- 5a Logout
```sh
url = http://127.0.0.1:8000/logout/
body = {}
headers = {}
response = requests.request("POST", url, headers=headers, data=body)
```
- 6 Share post, new post will create
```sh
url = http://127.0.0.1:8000/sharepost/
body = {'post_id': 2}
headers = {}
response = requests.request("POST", url, headers=headers, data=body)
```

## Test the API
#### There are two tests:
1. Python file
```sh
MPB\blog\tests.py
```
This Python file is running many test using unittest library.

2. Postman test
```sh
MPB\MPB.postman_tests.json
```
This JSON file can be imported to Postman, it contains requests for all the cases of the API.
