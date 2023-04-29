import requests

url = "https://twelve-data1.p.rapidapi.com/stocks"

querystring = {}

headers = {}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())