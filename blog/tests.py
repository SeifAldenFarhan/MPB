# from django.contrib.sites import requests
import requests

# Create your tests here.

# post_data = {'username': 'Seif5', 'email': 'Seif@gmail.com', 'password': 'Asia21'}
# response = requests.post('http://127.0.0.1:8000/register/', data=post_data)
# content = response.content
# print(content)

# post_data = {'username': 'Seif1', 'password': 'Asia21'}
# response = requests.post('http://127.0.0.1:8000/login/', data=post_data)
# content = response.content
# print(content)

# response = requests.post('http://127.0.0.1:8000/posts/')
# content = response.content
# print(content)

# like_data = {'user': 'Seif5', 'post': 'post1'}
# response = requests.post('http://127.0.0.1:8000/likepost/', like_data)
# content = response.content
# print(content)

url = "http://127.0.0.1:8000/login/"
body = {'username': 'soso', 'password': 'soso123'}

# headers = {
#     'Cookie': 'csrftoken=ie4dePf5F8E8b5ZujY9MHLNnHHreeCfCzea93uen5hLaoFb6smq6OdHab6CT0NBq; sessionid=usk6uke0h63evvjse8xr11hme7pfxxbn'
# }

response = requests.request("POST", url, data=body)

print(response.text)
