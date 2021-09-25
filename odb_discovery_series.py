#!/usr/bin/env python3

from requests_html import HTMLSession

session = HTMLSession()
url = "https://discoveryseries.org/topics/?cat=all"

r = session.get(url)
# Uncomment if html needs to render
# r.html.render(sleep=3, wait=1)

# Main container that holds the topics and series
topic_container = r.html.find('.search-results')[0]

# Topics and Series containers. Series containers hold the courses.
topics = topic_container.find('.top-tab')
series = topic_container.find('.blog-content')

# The number of topic and series containers should match
if len(topics) != len(series):
    print("Length of topics and series do not match\n")

for i in range(len(topics)):
    topic = topics[i].text
    courses = series[i].find('.front-display-text h2')
    if i == 0:
        print(f"{topic} has {len(courses)} courses")
        for course in courses:
            # if course == courses[0]:
            link = list(course.absolute_links)[0]
            # print(course.text)
            r = session.get(link)
            lessons = r.html.find('li.course-lesson')
            if lessons:
                print(f"\t{course.text} has {len(lessons)} lessons")
            else:
                print(f"\t{course.text} has 1 lesson")
    print(f"{topic} has {len(courses)} courses")
