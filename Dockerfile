FROM debian:latest

RUN apt-get update && apt-get install -y python-pip locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8

ENV LANG pt_BR.utf8

COPY ./src/ /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app


CMD [ "python", "./main.py" ]
