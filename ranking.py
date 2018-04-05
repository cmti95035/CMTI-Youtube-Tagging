import os
import csv
import argparse
from collections import Counter


CONFIDENCE = 0.5


def load_perm(file='vocabulary.csv'):
    with open(file, mode='r') as fp:
        reader = csv.reader(fp)
        header = next(reader, None)
        data = dict()
        for r in reader:
            data[r[0].strip()] = r[3].strip()
        return data


def load_temp(file, ind=1):
    with open(file, mode='r') as fp:
        reader = csv.reader(fp)
        header = next(reader, None)
        return list([i[ind] for i in reader])


def process_rows(rows):
    master = list()
    for r in rows:
        for (m, n) in zip(r.split(' ')[::2], r.split(' ')[1::2]):
            m, n = m.strip(), n.strip()
            try:
                n = float(n)
            except:
                n = 0.0
            if n > CONFIDENCE:
                master.append(m)

    return Counter(master)


def write_back_temp(file, rows, header=None):
    with open(file, mode='w') as fp:
        writer = csv.writer(fp)
        if header:
            writer.writerow(header)
        writer.writerows(rows)


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="name/path of the file to process")
args = ap.parse_args()

data = load_perm()
rows = load_temp(args.file)
counter = process_rows(rows)

data_to_wb = list()

for k, v in counter.most_common():
    data_to_wb.append([k, data.get(k, k), v])

write_back_temp(os.path.join(os.path.dirname(args.file), '{}_confidence_counted_sorted.csv'.format(os.path.splitext(args.file)[0])), data_to_wb)
print('Completed...')

