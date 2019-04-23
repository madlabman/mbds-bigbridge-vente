FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y install vim curl python3 python3-dev g++ libsasl2-dev
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
RUN pip install riak
RUN pip install cassandra-driver
RUN pip install pymongo
RUN pip install sasl thrift thrift_sasl PyHive

RUN apt-get -y install libaio1 unzip
RUN pip install cx_Oracle
RUN mkdir -p /opt/oracle
COPY instantclient-basic-linux.x64-18.5.0.0.0dbru.zip /opt/oracle
RUN unzip /opt/oracle/instantclient-basic-linux.x64-18.5.0.0.0dbru.zip -d /opt/oracle
RUN echo /opt/oracle/instantclient_18_5 > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

RUN pip install progressbar2
