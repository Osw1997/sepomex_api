FROM python:3.7.4

COPY requirements.txt ./requirements.txt
COPY config.py ./config.py
COPY wsgi.py ./wsgi.py

COPY Datos/ ./Datos
COPY Scripts/ ./Scripts
COPY sepomex/ ./sepomex



RUN pip install -r requirements.txt

CMD ["python", "./wsgi.py"]

# Build the docker image: docker build -t sepomex_api_flask -f dockerfile .
# Run:  docker run -d -p 2222:2222 sepomex_api_flask