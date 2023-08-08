FROM sdnm/cassini-sdnm:latest
WORKDIR /root

COPY dataplane.py /root/cassini-dataplane/sdnm_cassini/.

RUN  chmod +x /root/init-service.sh

CMD ["/bin/bash", "init-service.sh"]
