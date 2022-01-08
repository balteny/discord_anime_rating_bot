FROM python:3.10
WORKDIR /app
COPY /app .
RUN pip install -r ./requirements.txt
VOLUME /app/config
CMD python3 main.py
