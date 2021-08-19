#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from textwrap import fill
from os.path import join
from requests_html import HTMLSession
import os


def save_devotional_utmost(url, title, verse_text, paragraphs, author):

    devotional_dir = '/home/carl/.scripts/projects/odb_devotionals/devotionals/utmost'

    headers = [f'{fill(url)}\n\n', f'{fill(title)}\n\n', f'{fill(verse_text)}\n\n']
    content = [f'{fill(paragraph)}\n\n' for paragraph in paragraphs]
    author = f'{fill(author)}\n\n'

    title = title.replace('’','').replace(':','').replace(' ','_')
    title = title.replace('(','').replace(')','').replace('-','_')
    title = title.replace('?','').replace('.','')
    title = title.replace(',','').replace('!','')
    title = title.replace('“','').replace('”','')
    title = title.replace('$','')
    file_name = join(devotional_dir, f'utmost_{title}.txt')

    with open(file_name,'w') as file:
        file.writelines(headers)
        file.writelines(content)
        file.write(author)

def save_devotional_odb(url, title, verse_text, verse, todays_scripture, paragraphs, author, header, reflection, prayer):

    devotional_dir = '/home/carl/.scripts/projects/odb_devotionals/devotionals/odb'

    headers = [f'{fill(url)}\n\n', f'{fill(title)}\n\n', f'{fill(verse_text)}\n', f'{fill(verse)}\n\n', f'{fill(todays_scripture)}\n\n']
    content = [f'{fill(paragraph)}\n\n' for paragraph in paragraphs]
    author = f'{fill(author)}\n\n'
    prayer_box = [f'{fill(header)}\n\n', f'{fill(reflection)}\n\n', f'{fill(prayer)}\n']

    title = title.replace('’','').replace(':','').replace(' ','_')
    title = title.replace('(','').replace(')','').replace('-','_')
    title = title.replace('?','').replace('.','')
    title = title.replace(',','').replace('!','')
    title = title.replace('“','').replace('”','')
    title = title.replace('$','')
    file_name = join(devotional_dir, f'odb_{title}.txt')

    with open(file_name,'w') as file:
        file.writelines(headers)
        file.writelines(content)
        file.write(author)
        file.writelines(prayer_box)

def save_devotional_ymi(url, title, author, paragraphs):

    devotional_dir = '/home/carl/.scripts/projects/odb_devotionals/devotionals/ymi'

    headers = [f'{fill(url)}\n\n', f'{fill(title)}\n\n', f'Author: {fill(author)}\n\n']
    content = [f'{fill(paragraph)}\n\n' for paragraph in paragraphs]

    title = title.replace('’','').replace(':','').replace(' ','_')
    title = title.replace('(','').replace(')','').replace('-','_')
    title = title.replace('?','').replace('.','')
    title = title.replace(',','').replace('!','')
    title = title.replace('“','').replace('”','')
    title = title.replace('$','')
    file_name = join(devotional_dir, f'ymi_{title}.txt')

    with open(file_name,'w') as file:
        file.writelines(headers)
        file.writelines(content)

def save_errors(errors):

    save_file = '/home/carl/.scripts/projects/odb_devotionals/devotional_errors.txt'

    with open(save_file,'a') as file:
        url = errors[0]
        exception = errors[1]

        file.write(f'{url}\n{exception}\n\n')

def odb_url(session, url):

    try:
        r = session.get(url)

        r.html.render(sleep=3, wait=1)
        title = r.html.find('.devo-title')[0].text

        verse_area = r.html.find('.verseArea')

        try:
            verse_text = verse_area[0].find('p', first=True).text
            verse = verse_area[0].find('.rtBibleRef')[0].text

        except:
            verse_text = verse_area[0].find('p')[0].text
            verse = verse_area[0].find('div')[2].text

        todays_scripture = r.html.find('.devo-scriptureinsight')[0].text

        all_content = r.html.find('.content')
        content = all_content[0].find('div', first=True)
        paragraphs = [paragraph.text for paragraph in content.find('p')]
        author = all_content[0].find('.author')[0].text

        try:
            prayer_section = r.html.find('#prayer-component')
            header = prayer_section[0].find('h4', first=True).text
            reflection = prayer_section[0].find('.devo-reflection.devo-question')[0].text
            prayer = prayer_section[0].find('.devo-reflection.devo-prayer')[0].text

        except IndexError:
            header = (f'This article may not have a prayer section.\n')
            reflection = ''
            prayer = ''
            print(f'{header}')

        save_devotional_odb(url, title, verse_text, verse, todays_scripture, paragraphs, author, header, reflection, prayer)

    except Exception as e:
        save_errors([url,e])
        print(f'Error with {url}')
        print(e)

def utmost_url(session, url):

    try:
        r = session.get(url)
        r.html.render(sleep=3, wait=1)

        title = r.html.find('h2.entry-title', first=True).text

        article = r.html.find('article')
        author = article[0].find('h4')[0].text

        verse_box = r.html.find('#key-verse-box')
        verse_text = verse_box[0].find('h4')[0].text

        content = r.html.find('.post-content')
        paragraphs = [paragraph.text for paragraph in content[0].find('p')]

        save_devotional_utmost(url, title, verse_text, paragraphs, author)

    except Exception as e:
        save_errors([url,e])
        print(f'Error with {url}')
        print(e)

def ymi_url(session, url):

    try:
        r = session.get(url)
        r.html.render(sleep=3, wait=1)

        content = r.html.find('.entry-content-wrapper')
        title = content[0].find('h1', first=True).text
        author = content[0].find('.blog-author', first=True).text

        paragraphs = [paragraph.text for paragraph in content[0].find('p')]

        save_devotional_ymi(url, title, author, paragraphs)
    
    except Exception as e:
        save_errors([url,e])
        print(f'Error with {url}')
        print(e)

def main():

    url_file = '/home/carl/.scripts/projects/odb_devotionals/devotion_urls.txt'

    with open(url_file) as file:
        urls = file.readlines()

    session = HTMLSession()
    errors = []
    unclassified = []
    total_urls = len(urls)
    current_url = 0
    for url in urls:
        url = url.strip()
        pfinished = (current_url / total_urls) if current_url > 0 else 0
        print(f'Downloading URL {current_url} of {total_urls}\n{pfinished:.2%} finished')

        
        if 'odb.org' in url:
            odb_url(session, url)
        elif 'ymi.today' in url:
            ymi_url(session, url)
        elif 'utmost.org' in url:
            utmost_url(session, url)
        elif 'feedproxy.google.com' in url:
            odb_url(session, url)
        else:
            unclassified.append(url)

        current_url += 1


main()
