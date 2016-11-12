import requests
import json
headers = {'Content-Type': 'application/json'}
r = requests.get('http://5.9.127.172/politicka-partija',headers=headers)
datas=r.json()
print datas
for i in datas['politickePartije']:
    print i['id']
    print i['naziv']
r1=requests.get('http://5.9.127.172/poslanik?ime=' + "veroljub" + '%20' + "arsic" ,headers=headers)
datas1 = r1.json()
test=datas1.values()[0][0]['id']
print test