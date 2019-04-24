#!/bin/bash

# @see https://neo4j.com/developer/guide-import-csv
PERSON_FILE=/import/person_0_0.csv
POST_FILE=/import/post_0_0.csv
PERSON_KNOWS_PERSON_FILE=/import/person_knows_person_0_0.csv
POST_CREATED_BY_FILE=/import/post_hasCreator_person_0_0.csv

PERSON_HEADER=$(head -n 1 $PERSON_FILE)
PERSON_HEADER_MODIFIED=${PERSON_HEADER/id/:ID(Person)}
#PERSON_HEADER_MODIFIED=${PERSON_HEADER_MODIFIED/creationDate/creationDate:DATE}
PERSON_HEADER_MODIFIED=${PERSON_HEADER_MODIFIED/birthday/birthday:DATE}
sed s/$PERSON_HEADER/$PERSON_HEADER_MODIFIED/ $PERSON_FILE >> /tmp/person.csv

POST_HEADER=$(head -n 1 $POST_FILE)
POST_HEADER_MODIFIED=${POST_HEADER/id/:ID(Post)}
POST_HEADER_MODIFIED=${POST_HEADER_MODIFIED/length/length:INT}
sed s/$POST_HEADER/$POST_HEADER_MODIFIED/ $POST_FILE >> /tmp/post.csv

PERSON_KNOWS_PERSON_HEADER=$(head -n 1 $PERSON_KNOWS_PERSON_FILE)
PERSON_KNOWS_PERSON_HEADER_MODIFIED=${PERSON_KNOWS_PERSON_HEADER/Person.id/:START_ID(Person)}
PERSON_KNOWS_PERSON_HEADER_MODIFIED=${PERSON_KNOWS_PERSON_HEADER_MODIFIED/Person.id/:END_ID(Person)}
sed s/$PERSON_KNOWS_PERSON_HEADER/$PERSON_KNOWS_PERSON_HEADER_MODIFIED/ $PERSON_KNOWS_PERSON_FILE >> /tmp/person_knows_person.csv

POST_CREATED_BY_HEADER=$(head -n 1 $POST_CREATED_BY_FILE)
POST_CREATED_BY_HEADER_MODIFIED=${POST_CREATED_BY_HEADER/Post.id/:END_ID(Post)}
POST_CREATED_BY_HEADER_MODIFIED=${POST_CREATED_BY_HEADER_MODIFIED/Person.id/:START_ID(Person)}
sed s/$POST_CREATED_BY_HEADER/$POST_CREATED_BY_HEADER_MODIFIED/ $POST_CREATED_BY_FILE >> /tmp/post_has_creator.csv

rm -rf /var/lib/neo4j/data/databases/shop.db  # remove previous one

neo4j-admin import --mode csv --database=shop.db --id-type string \
    --nodes:Person /tmp/person.csv \
    --nodes:Post /tmp/post.csv \
    --relationships:KNOWS /tmp/person_knows_person.csv \
    --relationships:CREATE /tmp/post_has_creator.csv \
    --delimiter '|' \
    --ignore-missing-nodes true

# remove temp files
rm /tmp/person.csv \
    /tmp/post.csv \
    /tmp/person_knows_person.csv \
    /tmp/post_has_creator.csv
