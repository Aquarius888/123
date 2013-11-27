"""скрипт выкачивает музыку из аудиозаписей в папку со скриптом"""


import webbrowser
#import pickle #сериализация - представление объекта в виде надоба байтов
import urllib.parse
#import json
import urllib.request
import xml.etree.ElementTree as etree
#from html.parser import HTMLParser
#import re
import os
#from xml.dom.minidom import parseString
#from datetime import datetime, timedelta



webbrowser.open_new_tab("http://api.vk.com/oauth/authorize?client_id=3982282&scope=audio&redirect_uri=http://api.vk.com/blank.html&display=page&response_type=token")

red_html = input('redirected html: ') #вводим адрес на который нас перекидывают
aup = urllib.parse.parse_qs(red_html)#распарсим линк
aup['access_token'] = aup.pop('http://api.vk.com/blank.html#access_token')#подрезаем строку

#print (html)
print (aup)

urls = "https://api.vk.com/method/audio.get.xml?uid=" + aup['user_id'][0] + "&access_token=" + aup['access_token'][0]

print (urls)
page = urllib.request.urlopen(urls) #возвращает объект, похожий на объект файла
htm = page.read()
html = open("doc.xml", "w", encoding='UTF-8') #создаем файл с ключом байтовой записи
html.write(htm.decode('utf-8')) # записываем в файл
html.close()
#print (htm)


artist = []
title = []
down_url = []

doc = etree.parse("doc.xml")
root = doc.getroot()

#print(root.tag, root.attrib)
for audio in root.findall('audio'): #получаем список юрлов
    down_url = audio.find('url').text
    artist = audio.find('artist').text
    title = audio.find('title').text
    print (down_url)
    urllib.request.urlretrieve(down_url, filename=str(title)+".mp3") #качает в папку расположения скрипта




