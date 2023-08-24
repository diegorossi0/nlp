import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("https://www.vagalume.com.br/skank/")
soup = BeautifulSoup(page.content, 'html.parser')
lista_alfabetica = BeautifulSoup(str(soup.findChildren(id = "alfabetMusicList")), 'html.parser')
a_tag = lista_alfabetica.findAll('a')

musicas = []
for a in a_tag:
    nome_musica = a.text
    if not(nome_musica == 'TRADUÇÃO' or nome_musica == ''):
        link_musica = a['href']
        musicas.append([nome_musica, link_musica])
        
for i in range(len(musicas)):
    link = "https://www.vagalume.com.br" + str(musicas[i][1])
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    h3_tag = soup.findAll('h3')
    if len(h3_tag) != 0:
        album = h3_tag[0].text
    else:
        album = ''
    lyrics = soup.findChildren(id = 'lyrics')
    lyrics = str(lyrics[0])
    lyrics = lyrics.replace('<div id="lyrics">', '')
    lyrics = lyrics.replace('<div data-plugin="googleTranslate" id="lyrics">', '')
    lyrics = lyrics.replace('<br/>', ' ')
    lyrics = lyrics.replace("\'","'") 
    lyrics = lyrics.replace('</div>', '')
    musicas[i].append(album)
    musicas[i].append(lyrics)

musicas = pd.DataFrame(musicas, columns=['Nome da Música', 'link', 'album', 'letra'])
musicas.to_csv('musicas.csv', index=False)