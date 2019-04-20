FROM alpine:3.9.3

RUN apk add --no-cache vim curl python3 python3-dev g++ cyrus-sasl-dev cyrus-sasl-plain
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
RUN pip install riak
RUN pip install cassandra-driver
RUN pip install pymongo
RUN pip install sasl thrift thrift_sasl PyHive

