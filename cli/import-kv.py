import sys
import csv
import progressbar
import riak

try: # checking import file path argument existing
    filename = sys.argv[1]
    if len(filename) <= 0:
        raise Exception
except:
    print('You have to provide filename for import')
    sys.exit(-1)

try:
    client = riak.RiakClient(host = 'kv', pb_port = 8087) # connection to the riak
except Exception as error:
    print(error)
    sys.exit(-1)

try:
    with open(filename, 'r') as csvfile:
        filereader = csv.reader(csvfile, delimiter = '|', quotechar = '\'')
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        loaded_count = 0
        for row in filereader:
            bucketname, person_id, feedback = row # getting values from line
            bucket = client.bucket(bucketname) # creating new bucket with asin name
            bucket.new(person_id, data=feedback).store() # store feedback by id
            loaded_count += 1; bar.update(loaded_count) # show progress
        print('Data was loaded')
        sys.exit(0)
except Exception as error:
    print(error)
    sys.exit(-1)
