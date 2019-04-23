import sys
import argparse
import progressbar
import json
from pymongo import MongoClient

# defining arguments
parser = argparse.ArgumentParser(description='Import JSON to Mongo')
parser.add_argument('-f', nargs=1, required=True, help='path to the JSON file')
parser.add_argument('-c', nargs=1, required=True, help='name of collection to import')
args = parser.parse_args()  # parsing arguments

try:
    client = MongoClient('document', 27017)  # establishing connection
    db = client.test  # selecting database
    collection = db[args.c[0]]
    with open(args.f[0], 'r') as jsonfile:
        num_lines = sum(1 for line in jsonfile); jsonfile.seek(0, 0)  # calculating rows count
        bar = progressbar.ProgressBar(max_value=num_lines)
        loaded_count = 0
        for line in jsonfile:
            document = json.loads(line)  # loading JSON from line
            collection.insert_one(document)  # inserting document into collection
            loaded_count += 1; bar.update(loaded_count)
    bar.finish()  # for avoiding 99% status
    print('Data was loaded')
    sys.exit(0)
except Exception as error:
    print(error)
    sys.exit(-1)
