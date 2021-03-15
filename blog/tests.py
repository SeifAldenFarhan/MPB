import unittest

import requests


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

    def test_posts(self):
        response = requests.get(self.url + 'posts/', headers=self.headers).content
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
