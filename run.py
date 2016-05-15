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

def get_url_template(code, idx):
    url = URL.format(code + str(idx))
    logging.info('search link: ' + url)

    r = requests.get(url)
    jpg_url = re.search(r'http://.*?/mono/movie/adult/.*?jpg', r.text)
    if not jpg_url:
        return None
    url = jpg_url.group(0)

    if url[-6:] == 'ps.jpg':
        url = url[:-6] + 'pl.jpg'

    return re.sub(code + '\d{3}', code + '{0:0>3}', url, 2)


def download_images(code, start=1, stop=None):
    logging.info('start...')
    code = code.upper()
    start = int(start)
    stop = start + 10 if (stop is None) else int(stop)

    url = get_url_template(code.lower(), start)
    if url is None:
        exit()
    logging.info('url template => ' + url)

    # if directory is not exists, make directory
    image_dir = os.path.join(os.curdir, code)
    if not os.path.isdir(image_dir):
        os.mkdir(code)
    logging.info('download floder => ' + image_dir)

    for idx in range(start, stop):
        # check file exists
        file = os.path.join(image_dir, '{:0>3}.jpg'.format(idx))
        if os.path.isfile(file):
            continue

        image_url = url.format(idx)
        r = requests.get(image_url)
        # check status code
        if r.status_code != 200:
            logging.info('request status code is %s!' % r.status_code)
            break
        # check redirect
        if r.url != image_url:
            new_url = get_url_template(code.lower(), idx)
            if new_url is None:
                continue
            url = new_url
            logging.info('new url template => ' + url)
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
        print('Usage: ./run.py code start=1 stop=start+10')
        exit()

    kw = dict(zip(['code', 'start', 'stop'], argv))
    download_images(**kw)