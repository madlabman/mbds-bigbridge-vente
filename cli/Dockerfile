FROM alpine:3.9.3

RUN apk add --no-cache vim curl python3
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
RUN pip install riak
