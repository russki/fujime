FROM ubuntu:16.04

ADD . /fujime

# Commands
RUN \
  apt-get update && \
  apt-get install -y python-virtualenv && \
  virtualenv /venv && \
  /venv/bin/pip install -r /fujime/requirements.txt && \
  apt-get autoremove -y && \
  apt-get clean all

CMD ["/venv/bin/python", "/fujime/fujime.py", "--config", "/fujime/config.yaml"]
