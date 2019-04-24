import sys
import argparse
import progressbar
import csv
import progressbar
from neo4j import GraphDatabase

# defining arguments
parser = argparse.ArgumentParser(description='Import data to Neo4j')
parser.add_argument('-f', nargs=1, required=True, help='path to the import file')
parser.add_argument('-t', nargs='+', required=True, help='name of the entity tag')
parser.add_argument('--relation', nargs='?', help='enable relation import mode', default=False)
args = parser.parse_args()  # parsing arguments


def entity_tx(tx, obj):
    obj_struct = []
    for key in obj.keys():
        obj_struct.append('{}:{{{}}}'.format(key, key))
    obj_struct = ', '.join(obj_struct)  # generate statement structure
    statement = 'CREATE (:{} {{{}}})'.format(args.t[0], obj_struct)  # create statement
    tx.run(statement, obj)  # run transaction


def relation_tx(tx, row, fields):
    ids_offset = 2
    props = {}
    props_struct = []
    for i in range(0, len(fields)):
        props[fields[i]] = row[i + ids_offset]
        props_struct.append('{}:{{{}}}'.format(fields[i], fields[i]))
    props_struct = ', '.join(props_struct)
    statement = 'MATCH (a:{} {{id: \'{}\'}}), (b:{} {{id: \'{}\'}}) CREATE (a)-[:{} {{{}}}]->(b)'.format(args.t[0], row[0], args.t[1], row[1], args.relation, props_struct)
    tx.run(statement, props)

try:
    driver = GraphDatabase.driver('bolt://graph:7687', auth=('neo4j', 'neo4jpa55'))  # open connection
    session = driver.session()
    with open(args.f[0], 'r', encoding='utf-8') as csvfile:
        num_lines = sum(1 for line in csvfile) - 1; csvfile.seek(0, 0)  # calculating row count
        bar = progressbar.ProgressBar(max_value=num_lines)
        loaded_count = 0
        if not args.relation:
            filereader = csv.DictReader(csvfile, delimiter='|')
            for row in filereader:
                session.write_transaction(entity_tx, row)
                loaded_count += 1; bar.update(loaded_count)
        else:
            filereader = csv.reader(csvfile, delimiter='|')
            header = next(filereader)
            if len(header) < 2:  # check CSV header
                raise Exception('Relation require 2 entity')
            if len(args.t) < 2:  # check args count
                raise Exception('You have to provide 2 tags for realtion')
            props = []
            for idx, field in enumerate(header):
                parts = field.split('.')
                if not (len(parts) == 2 and parts[1] == 'id'):  # in case of field name does not contain .id
                    props.append(field)  # add field to the properties list
            for row in filereader:
                session.write_transaction(relation_tx, row, props)
                loaded_count += 1; bar.update(loaded_count)
        bar.finish()
        print('Data was loaded')
        sys.exit(0)
except Exception as error:
    print('\n')
    print(error)
    sys.exit(-1)
