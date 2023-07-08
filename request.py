import requests

url = 'http://localhost:4000/api/predict'
headers = {'Content-Type': 'application/json'}
data = {'image': 'https://heatlieletterboxes.com.au/cdn/shop/products/Bolt_On_Black_1.jpg?v=1644373922'}

response = requests.post(url, headers=headers, json=data)
print(response.text)
