#!/usr/bin/python3

from os.path import join
from requests_html import HTMLSession
from textwrap import fill
import os

def save_errors(errors):

    save_file = '/home/carl/.scripts/projects/odb_devotionals/odb_errors3.txt'

    with open(save_file,'a') as file:
        url = errors[0]
        exception = errors[1]

        file.write(f'{url}\n{exception}\n\n')

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
        

def testing_save_devotional_odb(url, title, verse_text, verse, todays_scripture, paragraphs, author, header, reflection, prayer):

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
    file_name = (f'odb_{title}.txt')

    print(file_name)

    for item in headers:
        print(item)
    
    for item in content:
        print(item)

    print(author)

    for item in prayer_box:
        print(item)

def testing_odb(session, url):

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

    testing_save_devotional_odb(url, title, verse_text, verse, todays_scripture, paragraphs, author, header, reflection, prayer)

def main():

    list_file = '/home/carl/.scripts/projects/odb_devotionals/odb_errors3.txt'

    with open(list_file) as file:
        urls = file.readlines()

    session = HTMLSession()

    total_urls = len(urls)
    current_url = 0
    for url in urls:
        url = url.strip()
        pfinished = (current_url / total_urls) if current_url > 0 else 0
        print(f'Downloading URL {current_url} of {total_urls}\n{pfinished:.2%} finished')
        odb(session, url)
        current_url += 1
        
def testing():

    session = HTMLSession()
        
    url = 'https://odb.org/2017/09/06/before-the-lord/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+odb%2Ffeed+%28Our+Daily+Bread%29'

    testing_odb(session, url)

main()
