FROM ubuntu:16.04

RUN apt-get update && apt-get -y install curl supervisor
RUN curl -s https://packagecloud.io/install/repositories/basho/riak/script.deb.sh | bash
RUN apt-get -y install riak=2.2.3-1

COPY ./riak.conf /etc/riak
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /var/log/supervisor

EXPOSE 8087 8098

CMD ["/usr/bin/supervisord"]
