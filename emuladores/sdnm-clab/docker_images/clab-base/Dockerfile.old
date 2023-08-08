FROM debian:bullseye as builder

RUN apt-get update \
    && apt install -y cargo git libcairo2-dev libgirepository1.0-dev make pkg-config python3-cairo python3-gi-cairo python3-pip \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git clone https://github.com/nispor/nispor \
    && cd nispor \
    && PREFIX=/usr make install \
    && pip3 install src/python/ \
    && pip3 wheel --wheel-dir=/root/wheels src/python/ nmstate==1.0.3

FROM jrei/systemd-debian:11

COPY --from=builder /usr/lib64/libnispor.so.1.* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /root/wheels /root/wheels

RUN apt-get update \
    && apt-get install -y gir1.2-nm-1.0 network-manager python3-pip \
    && openvswitch-switch python3-openvswitch openssh-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install \
      --no-index \
      --find-links=/root/wheels \
      nispor nmstate
RUN pip3 install varlink

