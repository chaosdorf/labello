FROM python:3.8-alpine

WORKDIR /app
COPY ./ ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "python", "./labelprinterServe.py" ]
