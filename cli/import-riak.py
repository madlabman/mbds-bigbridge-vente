import sys
import csv
import progressbar
import riak
import argparse

# defining arguments
parser = argparse.ArgumentParser(description='Import Feedback from CSV to Riak')
parser.add_argument('-f', nargs=1, required=True, help='path to the CSV file')
args = parser.parse_args()

try:
    client = riak.RiakClient(host='kv', pb_port=8087)  # connection to the riak
except Exception as error:
    print(error)
    sys.exit(-1)

try:
    with open(args.f[0], 'r') as csvfile:
        num_lines = sum(1 for line in csvfile); csvfile.seek(0, 0)  # calculate rows count
        filereader = csv.reader(csvfile, delimiter='|', quotechar='\'')
        bar = progressbar.ProgressBar(max_value=num_lines)
        loaded_count = 0
        for row in filereader:
            bucket_name, person_id, feedback = row  # getting values from line
            bucket = client.bucket(bucket_name)  # creating new bucket with asin name
            bucket.new(person_id, data=feedback).store()  # store feedback by composite key
            loaded_count += 1; bar.update(loaded_count)  # show progress
        bar.update()
        print('Data was loaded')
        sys.exit(0)
except Exception as error:
    print(error)
    sys.exit(-1)
