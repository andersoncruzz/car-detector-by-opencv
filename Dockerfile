FROM nuveo/opencv:alpine-python3-opencv3

RUN apk add build-base
RUN apk add --update bash && rm -rf /var/cache/apk/*

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
