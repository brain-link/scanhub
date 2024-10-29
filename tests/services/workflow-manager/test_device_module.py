import requests

file = {'file': open('/home/johnny99/Git/new/scanhub/tests/readme.txt','rb')}
url = "http://localhost:8080/api/v1/devices/test_device/result/test_result/"

r = requests.post(url, files=file)
print(r.json())