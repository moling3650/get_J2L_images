#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-14 23:56:20
# @Author  : moling


import re
import os
import sys
import urllib
import logging
import requests

logging.basicConfig(level=logging.INFO)
SEARCH_URL = 'http://www.javli6.com/cn/vl_searchbyid.php?keyword={}'


def get_valid_value(page_str):
    try:
        page = int(page_str)
    except ValueError:
        page = 1
    return max(page, 1)


def get_url_template(title, idx):

    link = SEARCH_URL.format(title + str(idx))
    logging.info('Search Url: ' + link)

    r = requests.get(link)
    jpg_url = re.search(r'http://.*?/mono/movie/adult/.*?jpg', r.text)
    if not jpg_url:
        return None
    url = jpg_url.group().replace('ps.jpg', 'pl.jpg')

    return re.sub('%s\d{3}' % title, '%s{0:0>3}' % title, url, 2)


def download_images(title, start=1, stop=None, outtime=10):
    logging.info('Start...')
    title = title.upper()
    start = get_valid_value(start)
    stop = start + 10 if (stop is None) else get_valid_value(stop) + 1
    outtime = get_valid_value(outtime)

    url = get_url_template(title.lower(), start)
    if url is None:
        exit()
    logging.info('Url template => ' + url)

    # if directory is not exists, make directory
    DL_dir = os.path.join(os.curdir, title)
    if not os.path.isdir(DL_dir):
        os.mkdir(title)
    logging.info('Download Dir => %s' % DL_dir)

    for idx in range(start, stop):
        # check file exists
        file = os.path.join(DL_dir, '{0}-{1:0>3}.jpg'.format(title, idx))
        if os.path.isfile(file):
            continue

        image_url = url.format(idx)
        r = requests.get(image_url)
        # check status code
        if r.status_code != 200:
            logging.info('Request status code is %s!' % r.status_code)
            break
        # check redirect
        if r.url != image_url:
            new_url = get_url_template(title.lower(), idx)
            if new_url is None:
                outtime -= 1
                if outtime == 0:
                    break
                continue
            url = new_url
            logging.info('New url template => ' + url)
            image_url = url.format(idx)
            r = requests.get(image_url)
        # download the file
        with open(file, 'wb') as f:
            f.write(r.content)
            logging.info('DL: %s => %s' % (image_url, file))

    logging.info('Done!')


def get_images_by_page(title, first_papg=1, last_page=1):
    logging.info('Start...')
    title = title.upper()
    start = get_valid_value(first_papg)
    stop = max(min(get_valid_value(last_page), 25), start) + 1
    URL_TEMPLATE = 'http://www.javli6.com/cn/vl_%s.php?&mode=&page={page}' % title.lower()
    DL_dir = os.path.join(os.curdir, title)
    if not os.path.isdir(DL_dir):
        os.mkdir(DL_dir)
    logging.info('Download Dir => %s' % DL_dir)
    for idx in range(start, stop):
        logging.info('Download page: %s' % idx)
        r = requests.get(URL_TEMPLATE.format(page=idx))
        jpgs = re.findall(r'<div class="id">(.+?)</div>.+?(http://.*?jpg)', r.text)
        for jpg in jpgs:
            file = os.path.join(DL_dir, '%03s.jpg' % (jpg[0]))
            if os.path.isfile(file):
                logging.info('%s was existed.' % (file))
                continue
            url = jpg[1].replace('ps.jpg', 'pl.jpg')
            urllib.urlretrieve(url, file)
            logging.info('DL: %s => %s' % (url, file))

    logging.info('Done!')


if __name__ == '__main__':
    category = {
        '-nr': 'newrelease',
        '-ne': 'newentries',
        '-m': 'mostwanted',
        '-b': 'bestrated'
    }
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./get_images.py title [start] [stop] [outtime]')
        print('Usage: ./get_images.py command [first_papg] [last_page]')
        print('commands: %s' % category)
        exit()

    key = argv[0].lower()
    if key in category.keys():
        argv[0] = category[key]
        kw = dict(zip(['title', 'first_papg', 'last_page'], argv))
        get_images_by_page(**kw)
    else:
        kw = dict(zip(['title', 'start', 'stop', 'outtime'], argv))
        download_images(**kw)
