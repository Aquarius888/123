import webbrowser
import urllib.parse
import urllib.request
import xml.etree.ElementTree as etree
import os

def get_xml():
    webbrowser.open_new_tab("""http://api.vk.com/oauth/authorize?client_id=3982282&scope=audio&redirect_uri=
http://api.vk.com/blank.html&display=page&response_type=token""")

    red_html = input('redirected html: ') #вводим адрес на который нас перекидывают
    aup = urllib.parse.parse_qs(red_html)#распарсим линк, словарь значений
    aup['access_token'] = aup.pop('http://api.vk.com/blank.html#access_token')#подрезаем строку

    urls = "https://api.vk.com/method/audio.get.xml?uid=" + aup['user_id'][0] + "&access_token=" + aup['access_token'][0]

    page = urllib.request.urlopen(urls) #возвращает объект, похожий на объект файла
    htm = page.read() #xml page type
    html = open("doc.xml", "w", encoding='UTF-8') #создаем файл с ключом байтовой записи
    html.write(htm.decode('utf-8')) #записываем в файл
    html.close()

def get_track_dict(root):
    artist = []
    title = []
    down_url = []
    track_dict = {}
    num = 0
    print("Список аудиозаписей:")
    for audio in root.findall('audio'): #получаем список юрлов
        num+=1
        down_url = audio.find('url').text
        artist = audio.find('artist').text
        title = audio.find('title').text
        print ('{0}. {1}{2}'.format(num, artist, title)) #получили список трэков

        track_dict[num] = (artist, title, down_url)
    return track_dict


def get_all_audio(root):

    for audio in root.findall('audio'):
        down_url = audio.find('url').text
        title = audio.find('title').text
        urllib.request.urlretrieve(down_url, filename=str(title)+".mp3")

def get_num_audio(save_track, track_dict):
    d_url = track_dict[int(save_track)]
    print("Качаем - {0}".format(d_url[0]))
    urllib.request.urlretrieve(d_url[2], filename='{1}.mp3'.format(d_url[0], d_url[1]))

def main():
    get_xml()
    doc = etree.parse("doc.xml")
    root = doc.getroot()
    track = get_track_dict(root)
    save_track = input("Введите номер скачиваемого трэка или <all> для загрузки всех аудиозаписей: ")
    if save_track == "all":
       get_all_audio(root)
    else: get_num_audio(save_track, track)

if __name__ == '__main__':
    main()
