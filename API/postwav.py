import requests
url = 'http://localhost:8081/endSentence'
headers = {
    'Content-Type': 'multipart/form-data'
}
files = {
    'file': ('test.wav', open('./data/test.wav', 'rb')),
}
response = requests.post(url=url, headers=headers, files=files)
print(response)
