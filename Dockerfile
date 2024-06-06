FROM infologistix/docker-selenium-python:alpine
WORKDIR /app

ENV X_USERNAME=user1294380
ENV X_USER_EMAIL=subhashishnabajja1575643@gmail.com
ENV X_PASSWORD=rvsB9,$x&.?m*fV


ENV MONGODB_USER_PASSWORD=flask_server_hash_1234
ENV MONGODB_USERNAME=flask_server
ENV MONGODB_APPNAME=Cluster0


ENV DELAY_WEBDRIVER=20
ENV DELAY_IMPLICIT=7

ENV HOST=0.0.0.0
ENV PORT=10000

COPY . .
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
EXPOSE 10000