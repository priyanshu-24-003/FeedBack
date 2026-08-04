FROM python:3.10-slim

#Creating a workdir named app The entire docker image is built on this Folder
WORKDIR /app

#Copying flask_app dir to the app dir
COPY flask_app/ /app/

#Copying models dir and vectoriizer file in the app dir
COPY models/vectorizer.pkl /app/models/vectorizer.pkl

#moving Credential file to working dir
COPY src/connections/credentials.py /app/src/connections/credentials.py

#exporting the dependencies in the docker image for our docker container to use.
#This requirements.txt is actually from inside the app.
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords wordnet


EXPOSE 5000

#local
CMD ["python", "app.py"]  

#Prod
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]