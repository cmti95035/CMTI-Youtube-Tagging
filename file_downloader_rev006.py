# -*- coding: utf-8 -*-
import os
import csv
import time
import random
import requests
from io import open
from tqdm import tqdm
from urllib import urlopen


INPUT_FILE = "links.csv"

tqdm.monitor_interval = 0


def parse_url_csv(file=INPUT_FILE):
    data = list()
    for _d in csv.DictReader(open(file, mode='r', encoding='utf-8', errors='ignore')):
        d = dict()
        for k, v in _d.items():
            d[k] = v.strip()

        if d not in data:
            data.append(d)
    return data


def download_from_url(url, path):
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    if os.path.exists(path):
        first_byte = os.path.getsize(path)
    else:
        first_byte = 0

    if first_byte >= file_size:
        return file_size

    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=path)
    req = requests.get(url, headers=header, stream=True)
    with(open(path, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


def file_downloader(folder, file, url, extension='mp4'):
    print('Downloading [{}] from [{}]...'.format(os.path.join(os.path.curdir, folder, '{}.{}'.format(file, extension)), url))
    if not os.path.isdir(os.path.join(os.path.curdir, folder)):
        os.makedirs(os.path.join(os.path.curdir, folder))
    for _ in range(2):
        try:
            download_from_url(url=url, path=os.path.join(os.path.curdir, folder, '{}.{}'.format(file, extension)),)
            return True
        except Exception as e:
            print('Error [{}] occurred, waiting for few seconds and retrying...'.format(e))
            time.sleep(random.randint(1, 3))
    print('Failed to download [{}], skipping...'.format(url))
    return False


def get_file_name(used, new):
    count = 1
    while True:
        if new in used:
            try:
                base, _ = new.rsplit('_', 1)
            except Exception as e:
                base = new
            new = '{:s}_{:03d}'.format(base, count)
            count += 1
            continue
        else:
            used.append(new)
            return used, new


if __name__ == '__main__':
    print('Script started...')
    input_data = parse_url_csv()
    print('Found {} files to download in total...'.format(len(input_data)))
    file_names = list()
    for d in input_data:
        file_names, fn = get_file_name(file_names, d['file'])
        file_downloader(url=d['url'], folder=d['folder'], file=fn)

    print('Script completed...')
