FROM infologistix/docker-selenium-python:alpine
WORKDIR /app


ENV HOST=0.0.0.0
ENV PORT=10000

COPY . .
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
EXPOSE 10000