#!/usr/bin/python3

import os
from os import listdir
from os.path import join
from shutil import copy2

odb_dir = '/home/carl/.scripts/projects/odb_devotionals/devotionals/odb/'
ymi_dir = '/home/carl/.scripts/projects/odb_devotionals/devotionals/ymi/'
utmost_dir = '/home/carl/.scripts/projects/odb_devotionals/devotionals/utmost/'

devotional_dir = '/home/carl/odb_devotionals/'

folder_num = 1

def create_folder():

    global folder_num

    folder = join(devotional_dir,f'folder_{folder_num}')

    if not os.path.exists(folder):
        os.mkdir(folder)

    folder_num +=1

    return folder
    
odb_devs = (join(odb_dir,file) for file in listdir(odb_dir))
ymi_devs = (join(ymi_dir,file) for file in listdir(ymi_dir))
utmost_devs = (join(utmost_dir,file) for file in listdir(utmost_dir))

odb_total = 0
ymi_total = 0
utmost_total = 0

full = False
while not full:

    folder = create_folder()
    odb_devotionals = 0
    ymi_devotionals = 0
    utmost_devotionals = 0

    while odb_devotionals < 50:
        try:
            copy2(next(odb_devs), folder)
            odb_devotionals += 1
            odb_total += 1
        except StopIteration:
            full = True
            break

    while ymi_devotionals < 10:
        try:
            copy2(next(ymi_devs), folder)
            ymi_devotionals += 1
            ymi_total += 1
        except StopIteration:
            break

    while utmost_devotionals < 10:
        try:
            copy2(next(utmost_devs), folder)
            utmost_devotionals += 1
            utmost_total += 1
        except StopIteration:
            break
