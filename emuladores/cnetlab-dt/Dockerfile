FROM docker

WORKDIR  /root/

RUN apk add python3 py3-pip git \
    && pip3 install pyyaml

RUN git clone https://github.com/lbors/dtn-sdn.git \
    && cd dtn-sdn/emuladores/cnetlab-dt/ \
    && python3 setup.py install
 