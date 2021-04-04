FROM ubuntu:20.04
RUN apt update && apt -y install python3 python3-pip && pip3 install requests
COPY . .
ENTRYPOINT ["python3", "fordpass.py", "-j"]
