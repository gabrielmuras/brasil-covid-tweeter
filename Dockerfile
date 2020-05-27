FROM python:3

COPY ./src /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app

CMD [ "python", "./main.py" ]
