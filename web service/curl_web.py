import requests

r = requests.get('https://www.seznam.cz')
r.headers['content-type']
r.json()
