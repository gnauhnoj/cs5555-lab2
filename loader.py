import csv
import logging
from collections import defaultdict
from config import export

logging.basicConfig(filename='loader.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Person(object):
    def __init__(self):
        self.info = {}
        self.person_id = None
        self.chronic = False


def load_info(filename, rows):
    """
    Loads data
    : param filename:
    : return:
    """
    header = True
    headers = {}
    check_len = None
    with open(filename,  'rb') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if header:
                for i, key in enumerate(row):
                    headers[i] = key
                header = False
                check_len = len(row)
            elif check_len == len(row):
                pid = int(row[0])
                rows[pid].person_id = pid
                for i, value in enumerate(row):
                    code = headers[i]
                    if code in export:
                        code = export[code]
                        rows[pid].info[code] = num(value)
                        if 'chronic_'in code and not rows[pid].chronic and rows[pid].info[code] is 1:
                            rows[pid].chronic = True
            else:
                logging.exception("length check failed :  " + str(row))
    logging.info("number of rows: " + str(len(rows)))
    for c in rows.itervalues():
        logging.info('\t'.join([str(c.person_id), str(len(c.info))]))
        break


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def load_raw(filename):
    rows = defaultdict(Person)
    load_info(filename, rows)
    return rows

if __name__ == '__main__':
    file = '2012-Consolidated-stripped.csv'
    rows = load_raw(file)
    print rows[37210103].info, rows[37210103].person_id, rows[37210103].chronic
    # file2 = 'MEPS-HC155_2012-MC.csv'
    # rows = load_raw(file2)
    # print rows[38947].info, rows[38947].person_id
