import re
import csv
import argparse


def load_perm(file='vocabulary.csv'):
    with open(file, mode='r') as fp:
        reader = csv.reader(fp)
        header = next(reader, None)
        data = dict()
        for r in reader:
            data[r[0].strip()] = r[3].strip()
        return data


def load_temp(file):
    with open(file, mode='r') as fp:
        reader = csv.reader(fp)
        header = next(reader, None)
        return header, list(reader)


def process(s, data):
    s_list = s.split(' ')
    for ind, si in enumerate(s_list):
        if si in data:
            s_list[ind] = data[si]
    return ' '.join(s_list)


def edit_rows(rows, data, ind=1):
    for r in rows:
        r[ind] = process(r[ind], data)
    return rows


def write_back_temp(file, header, rows):
    with open(file, mode='w') as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        writer.writerows(rows)


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="name/path of the file to process")
args = ap.parse_args()

data = load_perm()
header, rows = load_temp(args.file)
rows = edit_rows(rows, data)
write_back_temp(args.file, header, rows)
print('Completed...')