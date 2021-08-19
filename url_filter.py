#!/usr/bin/python3

url_file = 'url_list2.txt'

with open(url_file) as file:
    urls = file.readlines()

urls = [url.strip() for url in urls]

unique_urls = list(set(urls))

roots = []
misc = []

ymi_today = []
odb = []
ourdailybread = []
discoveryseries = []
feedproxy_google = []
wonder_of_creation = []
discover_the_word = []
ymi_blogging = []
christian_university = []
questions = []
utmost = []
feeds_feedburner = []
unsorted = []

for url in unique_urls:
    try:
        root = url.split('/')[2]
        if root == 'ymi.today':
            ymi_today.append(url)
        elif root == 'odb.org':
            odb.append(url)
        elif root == 'ourdailybread.org':
            ourdailybread.append(url)
        elif root == 'discoveryseries.org':
            discoveryseries.append(url)
        elif root == 'feedproxy.google.com':
            feedproxy_google.append(url)
        elif root == 'wonderofcreation.org':
            wonder_of_creation.append(url)
        elif root == 'discovertheword.org':
            discover_the_word.append(url)
        elif root == 'ymiblogging.org':
            ymi_blogging.append(url)
        elif root == 'christianuniversity.org':
            christian_university.append(url)
        elif root == 'questions.org':
            questions.append(url)
        elif root == 'utmost.org':
            utmost.append(url)
        elif root == 'feeds.feedburner.com':
            feeds_feedburner.append(url)
        else:
            unsorted.append(url)

    except IndexError:
        misc.append(url)

unique_urls2 = [element for element in unique_urls]
for item in misc:
    if item in unique_urls:
        unique_urls2.remove(item)

sorted_urls = [ymi_today, odb, ourdailybread, discoveryseries, feedproxy_google, wonder_of_creation,
        discover_the_word, ymi_blogging, christian_university, questions, utmost, feeds_feedburner]

years = []
odb_videos = []
for url in odb:
    year = url.split('/')[3]
    if year == 'video':
        odb_videos.append(url)
    else:
        years.append(year)

odb2 = [element for element in odb]

for video in odb_videos:
    if video in odb:
        odb2.remove(video)

years = list(set(years))
years.sort()

print(f'ymi_today {len(ymi_today)}')
print(f'ymi_blogging {len(ymi_blogging)}')
print(f'odb {len(odb2)}')
print(f'odb videos {len(odb_videos)}')
print(f'ourdailybread {len(ourdailybread)}')
print(f'discoveryseries {len(discoveryseries)}')
print(f'discover_the_word {len(discover_the_word)}')
print(f'feedproxy_google {len(feedproxy_google)}')
print(f'feeds_feedburner {len(feeds_feedburner)}')
print(f'wonder_of_creation {len(wonder_of_creation)}')
print(f'christian_university {len(christian_university)}')
print(f'questions {len(questions)}')
print(f'utmost {len(utmost)}')

total = 0
for item in ymi_today, odb2, utmost:
    total += len(item)
print(total)
print("4,442 if you include feedproxy")
print("Down from 12,074")

with open('devotion_urls.txt','w') as file:
    for item in ymi_today, odb2, feedproxy_google, utmost:
        for element in item:
            file.write(f'{element}\n')
