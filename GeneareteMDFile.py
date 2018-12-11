#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = 'runningapple'

import sys
import time


def read_file_name():
    try:
        return sys.argv[1] + '.md'
    except IndexError:
        print('please input file name')
    return None


def create_template():
    return '---' + \
           '\nTitle: YourBlogTitle' + \
           '\nDate: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + \
           '\nModified: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + \
           '\nComments: false' + \
           '\nCategory: Category' + \
           '\nTags: Tags' + \
           '\nSlug: ' + sys.argv[1] + \
           '\nAuthor: 苍南竹竿君' + \
           '\nStatus: draft' + \
           '\n---'


def create_file(filename, template):
    file = open('./content/' + filename, mode='w')
    file.write(template)
    file.close()


def generate_md_file():
    filename = read_file_name()
    if filename is not None:
        template = create_template()
        create_file(filename, template)


generate_md_file()
