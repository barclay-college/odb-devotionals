#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

def save_urls(url_list):

    url_file = 'url_list2.txt'

    with open(url_file, 'a') as file:
        for url in url_list:
            file.write(f'{url}\n')

def get_topics(session):

    topics = []
    url = 'https://ourdailybread.org/all-topics/'

    r = session.get(url)

    ts = r.html.find('.topic-view-all')
    for topic in ts:
        topic = topic.text.replace('& ','').replace("'",'').replace(' ','-')
        topic = topic.lower()
        topics.append(topic)

    return topics

def scrape_devotionial_urls(response):

    url_list = []

    html_text = response.text

    soup = BeautifulSoup(html_text, 'lxml')

    panel_bodies = soup.find_all('div', class_='panel-body')

    for panel in panel_bodies:
        url = panel.find('a')['href']
        url_list.append(url)

    save_urls(url_list)

def main():


    session = HTMLSession()

    topics = get_topics(session)

    for topic in topics:
        page_num = 1
        cycle = True
        while cycle:
            url = f'https://ourdailybread.org/topics/{topic}/page/{page_num}/api/list/posts_per_page/15/sort[post_date]/DESC/'
            response = requests.get(url)
            status_code = response.status_code
            if status_code == 200:
                print(f'Topic: {topic}\nPage Number: {page_num}')
                scrape_devotionial_urls(response)
                page_num += 1

            else:
                cycle = False

#main()
get_topics2()
