import requests

url = "https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyBRcLVFSE044zGdn-K0VL1cjRfiheFm5Ss"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)