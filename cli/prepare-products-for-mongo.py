import sys
import mmap
import csv
import argparse
import os
import json
import progressbar

parser = argparse.ArgumentParser(description='Combine two CSV files into JSON to upload into Mongo')
parser.add_argument('product', help='Product.csv')
parser.add_argument('brand_by_product', help='BrandByProduct.csv')
parser.add_argument('-o', nargs=1, required=True, help='output filename')
args = parser.parse_args()  # parsing arguments

try:
    brand_by_product_file = open(args.brand_by_product, 'r')
    brand_map = mmap.mmap(brand_by_product_file.fileno(), 0, prot=mmap.PROT_READ)
    output_file = open(args.o[0], 'w+')
    product_file = open(args.product, 'r')
    num_lines = sum(1 for line in product_file) - 1; product_file.seek(0, 0)
    filereader = csv.DictReader(product_file)
    bar = progressbar.ProgressBar(max_value=num_lines)
    loaded_count = 0
    found_count = 0
    for row in filereader:
        asin = row['asin']
        asin_index = brand_map.find(asin.encode('utf-8'))
        if (asin_index > 0):
            line_start_index = brand_map.rfind(os.linesep.encode('utf-8'), asin_index - 128, asin_index)
            if line_start_index != -1:
                brand_map.seek(line_start_index + 1, 0)
                brand_line = brand_map.readline().decode('utf-8')
                row['brand'] = brand_line.split(',')[0]  # getting brand line from string
                found_count += 1
        json.dump(row, output_file)  # dumping json into output file
        output_file.write('\n')
        loaded_count += 1; bar.update(loaded_count)
        brand_map.seek(0, 0)  # seek map to the beginning of the file
    bar.finish()
    if num_lines == found_count:
        print('Data exported')
    else:
        print('Found only {} from {}'.format(found_count, loaded_count))
    brand_by_product_file.close()
    product_file.close()
    sys.exit(0)
except Exception as error:
    print(error)
    sys.exit(-1)
