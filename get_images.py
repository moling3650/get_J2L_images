#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-14 23:56:20
# @Author  : moling


import re
import os
import sys
import logging
import requests

logging.basicConfig(level=logging.INFO)
URL = 'http://www.javli6.com/cn/vl_searchbyid.php?keyword={}'


def get_valid_value(num_string):
    try:
        return max(int(num_string), 1)
    except ValueError:
        return 1


def get_url_template(code, idx):

    link = URL.format(code + str(idx))
    logging.info('Search link: ' + link)

    r = requests.get(link)
    jpg_url = re.search(r'http://.*?/mono/movie/adult/.*?jpg', r.text)
    if not jpg_url:
        return None
    url = jpg_url.group(0)

    if url[-6:] == 'ps.jpg':
        url = url[:-6] + 'pl.jpg'

    return re.sub(code + '\d{3}', code + '{0:0>3}', url, 2)


def download_images(code, start=1, stop=None, outtime=10):
    logging.info('Start...')
    code = code.upper()
    start = get_valid_value(start)
    stop = start + 10 if (stop is None) else get_valid_value(stop) + 1
    outtime = get_valid_value(outtime)

    url = get_url_template(code.lower(), start)
    if url is None:
        exit()
    logging.info('Url template => ' + url)

    # if directory is not exists, make directory
    DL_dir = os.path.join(os.curdir, code)
    if not os.path.isdir(DL_dir):
        os.mkdir(code)
    logging.info('Download floder => ' + DL_dir)

    for idx in range(start, stop):
        # check file exists
        file = os.path.join(DL_dir, '{:0>3}.jpg'.format(idx))
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
            new_url = get_url_template(code.lower(), idx)
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

if __name__ == '__main__':

    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./get_images.py code [start] [stop] [outtime]')
        exit()
    kw = dict(zip(['code', 'start', 'stop', 'outtime'], argv))
    download_images(**kw)