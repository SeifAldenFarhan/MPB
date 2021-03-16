# MPB
## Setup

### It is possible to run the image on a new instance.
#### The Hub Docker [Repository](https://hub.docker.com/repository/docker/315301580/mpb_image).
1. Open your browser to [Play with Docker](https://labs.play-with-docker.com/).
2. Click Login and then select docker from the drop-down list.
3. Connect with your Docker Hub account.
4. Once you’re logged in, click on the ADD NEW INSTANCE option on the left side bar. If you don’t see it, make your browser a little wider. After a few seconds, a terminal window opens in your browser.
5. In the terminal, start your freshly pushed app.
```sh
 docker run -dp 3000:3000 315301580/mpb_image
```
You should see the image get pulled down and eventually start up!
6.Click on the 3000 badge when it comes up and you should see the app with your modifications! Hooray! If the 3000 badge doesn’t show up, you can click on the “Open Port” button and type in 3000.


### The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/SeifAldenFarhan/MPB.git
$ cd MPB
```

### Create a virtualenv and install Django and any other requirements
In your Bash console, create a virtualenv, naming it after your project, and choosing the version of Python you want to use:
```sh
$ py -m pip install --user virtualenv
$ py -m venv myproject
$ .\myproject\Scripts\activate
(myproject)$ pip install -r requirements.txt
```

### Once pip has finished downloading the dependencies:
### Set Database (Make Sure you are in directory same as manage.py)
```sh
(myproject)$ cd MPB
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create SuperUser
```sh
$ python manage.py createsuperuser
```
### Run the project
```sh
(myproject)$ python manage.py runserver
```

#### After all these steps , you can start testing this project.

## About the project
First of all, the user needs to register to use the other functions.
Then, the user login by his/her username and password.
After the login, the user can see all the blogs, can write a new blog(post), and edit or delete it if and only if he/she is the author.
Also, the user can like the others' posts or unlike (if he/she like the posts already).
The user can share the other's posts.
In the end, the user can logout.

## About the project - technical
#### The project is using:
1. Restful API for a part of the project.
2. Using python, and ORM.
3. Tests (Python unittest/Postman).
4. Perfect Error handling.
5. Containerize the application using docker.
6. Errors should be handled gracefully.

## The Database
#### The used database is SQL (SQLite):
- Easy to setup, light-weight, more of a single-user or low volume database.
- All data is stored in a file which is easy to transfer from system to system.
- No server setup needed.
- Support ORM (Object–relational mapping).
- Fast enough, gets the job done.
- The default database when starting a new Django project.
- NoSql is 3rd party, not built-in and needs to setup.
- NoSql doesn't support ManyToManyFields and has a few other limitations.

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
url = http://127.0.0.1:8000/posts/
headers = {'Cookie': } // can get after user login
response = requests.request("GET", url, headers=headers)
```

- 2 APIs to allow all users to like posts.
```sh
url = http://127.0.0.1:8000/likepost/
body = {'post_id': 1}
headers = {'Cookie': } // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```

- 2a Only the user that liked the post can remove his like.
```sh
url = http://127.0.0.1:8000/unlikepost/
body = {'post_id': 1}
headers = {'Cookie': } // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 3 APIs to allow some users to post blog posts.
```sh
url = http://127.0.0.1:8000/newpost/
body = {'post_content': 'Hi, I am a new post'}
headers = {'Cookie': } // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 3a1 Only the users that wrote/posted the blog post can edit
```sh
url = http://127.0.0.1:8000/editpost/
body = {'post_id': 1, 'new_content': 'new content'}
headers = {'Cookie': } // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 3a2 delete the post.
```sh
url = http://127.0.0.1:8000/deletepost/
body = {'post_id': 1}
headers = {'Cookie': } // can get after user login
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
headers = {'Cookie': } // can get after user login
response = requests.request("POST", url, headers=headers, data=body)
```
- 6 Share post, new post will create
```sh
url = http://127.0.0.1:8000/sharepost/
body = {'post_id': 2}
headers = {'Cookie': } // can get after user login
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

***

_This repository was generated by Seif-alden Farhan, on March 16, 2021