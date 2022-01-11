from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import os, requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    results = []

    req = requests.get('https://gogoanime.run/?page=1').text
    soup = BeautifulSoup(req, 'lxml')
    animeUl = soup.find('ul', class_ = 'items')
    animeList = animeUl.find_all('li')
    for animes in animeList:
        anime = animes.find('div', class_ = 'img')
        title = anime.find('a')['title']
        id = anime.find('a')['href'][1:]
        image = anime.find('img')['src']
        episodeNumber = id.split('episode-')[1]
        finalId = id.split('-episode-')[0]

        result = {'title': title, 'id': finalId, 'image': image, 'ep': episodeNumber}
        results.append(result)


    return jsonify({'results': results})

@app.route('/details/<id>', methods=['GET'])
def details(id):
    summary = ""
    status = ""
    released = ""

    req = requests.get('https://gogoanime.run/category/' + id).text
    soup = BeautifulSoup(req, 'lxml')
    episodes = soup.find('ul', id='episode_page')
    totalEp = int(episodes.find_all('a')[-1]['ep_end'])
    info = soup.find('div', class_ = 'anime_info_body_bg')
    image = info.find('img')['src']
    title = info.find('h1').text.strip()
    type = info.find_all('p', class_ = 'type')
    for item in type:
        span = item.find('span').text.strip()
        if(span == 'Plot Summary:'):
            summary = item.text.strip()[14:]
        elif(span == 'Status:'):
            status = item.text.strip()[8:]
        elif(span == 'Released:'):
            released = item.text.strip()[10:]

    return jsonify({'totalEp': totalEp, 'summary': summary, 'status': status, 'released': released, 'title': title, 'image': image, 'id': id})

if __name__ == '__main__':
    app.run(debug=True)