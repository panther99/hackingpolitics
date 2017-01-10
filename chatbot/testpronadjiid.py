#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json



def pronadjiid(name,last_name):
    headers = {'Content-Type': 'application/json'}
    r = requests.get('http://www.istinomer.rs/api/akter?show=all',headers=headers)
    datas=r.json()

    #print datas
    for i in datas:
       if unicode(i['ime'])==name and unicode(i['prezime']):
         return i['id']
         

#name=unicode("Siniša")
#prezime=unicode("Mali")
print pronadjiid(u'Sini',u'Mali')
