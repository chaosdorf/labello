FROM alpine

RUN apk --update add py-pip

WORKDIR /app
COPY ./ ./
RUN pip install -r requirements.txt

ENV PYTHONIOENCODING = utf-8

EXPOSE 8000
CMD [ "python", "./labelprinterServe.py" ]
