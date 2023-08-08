FROM sdnm/stratum:latest

WORKDIR /root

ENV PYTHONPATH $PYTHONPATH:/root

EXPOSE 50001

EXPOSE 22

COPY entrypoint.sh .

#COPY gencfg.py .

CMD ["/bin/bash", "entrypoint.sh"]
