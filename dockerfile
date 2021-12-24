FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
ENV DISCORD_TOKEN=<TOKEN>
CMD python3 main.py
