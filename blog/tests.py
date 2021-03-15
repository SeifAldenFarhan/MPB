# from django.contrib.sites import requests
import unittest

import requests


# Create your tests here.
class TestStringMethods(unittest.TestCase):
    url = 'http://127.0.0.1:8000/'
    headers = {
        'Cookie': 'csrftoken=pVVDQWoxUif0LvXH4g9wepei93i6sDoRBk5s673ViAQSbivMQoo094wXTm2nHnYV; '
                  'sessionid=0hc40q4pqbp9cbaglnp22g4g82nu9o47'
    }

    def test_register(self):
        post_data = {'username': 'Seif2021', 'password': 'seif123', 'email': 'seif@gmail.com'}
        response = requests.post(self.url + 'register/', data=post_data).content
        self.assertNotEqual(response, b'{"username": "Seif2021", '
                                      b'"email": "seif@gmail.com", "registered": true}')

    def test_login(self):
        post_data = {'username': 'Seif2021', 'password': 'seif123'}
        response = requests.post(self.url + 'login/', data=post_data).content
        self.assertEqual(response, b'{"username": "Seif2021", "email": "seif@gmail.com"}')

    def test_like_post(self):
        post_data = {'post_id': 1}
        response = requests.post(self.url + 'likepost/', headers=self.headers, data=post_data).content
        self.assertEqual(response, b'{"user": "Seif2021", '
                                   b'"post": {"post_id": 1, "author": "Asma", '
                                   b'"post_content": "Hi, this is the first post!"}}')


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

body = {'username': 'soso', 'password': 'soso123'}

# headers = {
#     'Cookie': 'csrftoken=ie4dePf5F8E8b5ZujY9MHLNnHHreeCfCzea93uen5hLaoFb6smq6OdHab6CT0NBq; sessionid=usk6uke0h63evvjse8xr11hme7pfxxbn'
# }
#
# response = requests.request("POST", url, data=body)
#
# print(response.text)


if __name__ == '__main__':
    unittest.main()
