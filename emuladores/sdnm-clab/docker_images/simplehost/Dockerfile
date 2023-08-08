FROM sdnm/clab-debian:11
RUN apt-get update
RUN apt-get install -y iperf3 tcpdump iputils-ping net-tools nano ethtool iproute2  bash

WORKDIR /root

COPY init-service.sh .
COPY host_network.service /lib/systemd/system/

ENV TERM=vt100
ENV PS1="[sdnm:host \u@\h]# "

LABEL br.rnp.label.name="host"\
      br.rnp.label.description="Simple Host Computer"\
      br.rnp.label.vendor="National Network for Education and Research - RNP"\
      br.rnp.label.contact="fernando.farias@rnp.br"\
      br.rnp.label.application="CNetLab"\
      br.rnp.label.version="0.1"\
      br.rnp.label.license="Apache2"

RUN  ln -sf /lib/systemd/system/host_network.service  /etc/systemd/system/multi-user.target.wants/host_network.service

#CMD [ "/bin/bash" ]

CMD ["/lib/systemd/systemd"]
