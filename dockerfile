FROM python:3.10
WORKDIR /app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt
VOLUME /app/config
CMD python3 main.py
