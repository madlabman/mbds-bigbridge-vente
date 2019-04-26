import sys
import progressbar
import argparse
import xml.etree.ElementTree as ET
import csv

# defining arguments
parser = argparse.ArgumentParser(description='Prepare XML invoice data for import to Cassandra')
parser.add_argument('xml_file', help='path to the data file')
parser.add_argument('-o', nargs=2, required=True, help='path to the output files')
args = parser.parse_args()

invoice_outfile = open(args.o[0], 'w')
orderline_outfile = open(args.o[1], 'w')
invoice_header_written = False
orderline_header_written = False

print('Parsing XML file...')
tree = ET.parse(args.xml_file)
root = tree.getroot()
nodes_count = len(root)
read_count = 0
bar = progressbar.ProgressBar(max_value=nodes_count)
for invoice in root:
    elem_obj = {}
    for elem in invoice:
        if elem.tag == 'OrderId':
            order_id = elem.text
        else:
            if elem.tag == 'Orderline':
                orderline_obj = {}
                for orderline_data in elem:
                    orderline_obj[orderline_data.tag] = orderline_data.text
                if 'order_id' in locals():
                    orderline_obj['orderId'] = order_id
                    orderline_fields = list(sorted(orderline_obj.keys()))
                    orderline_obj['orderlineId'] = order_id + '-' + orderline_obj['asin']
                    orderline_fields = ['orderlineId'] + orderline_fields;
                    if not orderline_header_written:
                        orderline_outfile.write(','.join(orderline_fields) + '\n')
                        orderline_header_written = True
                    w = csv.DictWriter(orderline_outfile, orderline_fields,
                                       delimiter=',',
                                       quotechar='"',
                                       quoting=csv.QUOTE_NONNUMERIC)
                    w.writerow(orderline_obj)
            else:
                elem_obj[elem.tag] = elem.text
    if 'order_id' in locals():
        invoice_fields = list(elem_obj.keys())
        elem_obj['OrderId'] = order_id
        invoice_fields = ['OrderId'] + invoice_fields
        if not invoice_header_written:
            invoice_outfile.write(','.join(invoice_fields) + '\n')
            invoice_header_written = True
        w = csv.DictWriter(invoice_outfile, invoice_fields,
                           delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        w.writerow(elem_obj)
    read_count += 1; bar.update(read_count)

bar.finish()
print('Data was prepared for import')
invoice_outfile.close()
orderline_outfile.close()
