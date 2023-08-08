FROM debian:bullseye as builder

RUN mkdir /build \
    && cd /build \
    && echo "deb-src http://deb.debian.org/debian bullseye main" >> /etc/apt/sources.list \
    && apt update \
	&& apt install -y cargo dpkg-dev git libcairo2-dev libgirepository1.0-dev make pkg-config python3-cairo python3-gi-cairo python3-pip \
	&& apt source network-manager \
	&& apt build-dep -y network-manager \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN cd /build/network-manager-1.30.0 \
    && sed -i 's,disable-ovs,enable-ovs,' debian/rules \
    && sed -i 's,NetworkManager.service,NetworkManager.service\nlib/systemd/system/NetworkManager.service.d/NetworkManager-ovs.conf,' debian/network-manager.install \
    && DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -rfakeroot -b 
	
RUN git clone https://github.com/nispor/nispor
RUN cd nispor \
    && PREFIX=/usr make install \
    && pip3 install src/python/ \
    && pip3 wheel --wheel-dir=/root/wheels src/python/ nmstate==1.0.3

FROM jrei/systemd-debian:11

#COPY --from=builder /usr/lib64/\\`ls -l /usr/lib64//libnispor.so | awk '{print $11}'\\` /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib64/libnispor.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /root/wheels /root/wheels
COPY --from=builder /build/network-manager_1.30.0-2_amd64.deb /root/

RUN apt-get update \
    && apt install -y --allow-downgrades /root/network-manager_1.30.0-2_amd64.deb ethtool gir1.2-nm-1.0 openvswitch-switch python3-pip python3-openvswitch \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install \
      --no-index \
      --find-links=/root/wheels \
      nispor nmstate
RUN pip3 install varlink

RUN sed -i 's/openvswitch/openvswitch-switch/' /usr/local/lib/python3.9/dist-packages/libnmstate/ifaces/ovs.py
