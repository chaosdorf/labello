FROM python:2-onbuild
EXPOSE 8000
CMD [ "python", "./labelprinterServe.py" ]
