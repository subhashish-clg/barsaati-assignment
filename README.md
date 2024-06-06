# Barsaati Media Assignment

## Problem Statement

Web scraping with Selenium and ProxyMesh, storing the data in MongoDB, showing a list on a webpage. This task will test your ability to work with web automation tools, proxies, and data extraction techniques.

## Introduction

The following video shows the working of the scraping script.
[Watch the video](https://drive.google.com/file/d/1Pay95pZm5YiMxUian4pf7bbghLlMZD7T/preview)

## Environment varialbes

The following are some of the important variables that you need to define.

```bash
X_USERNAME=...
X_USER_EMAIL=...
X_PASSWORD=...


MONGODB_USER_PASSWORD=...
MONGODB_USERNAME=...
MONGODB_APPNAME=...

# This has be defined if you are using proxies (this could be URL provided by ProxyMesh).
PROXY=....

# These can be left as it is
DELAY_WEBDRIVER=20
DELAY_IMPLICIT=7

HOST=0.0.0.0
PORT=10000
```

## How does this works

For the sake of simplicity I've connected the deployed frontend (React Application) with the `MongoDB` database, which shows trends according to my account.

For scraping the web you need to run the server locally and then enter the server URL, eg. "http://localhost:5000" in the alert box and then the scraping takes place.

## Setting up the local server

The following are the steps to run the `Flask` server.

1. Create a virtual environment (optional) by,

   ```bash
   python -m venv .venv # Note: You can use conda as well
   ```

2. Now run the server using the following command,

   ```bash
   flask --app server run
   ```

## Limitations with the approach

The following are the limitation of using this approach.

1. As it uses web scraping with `selenium` it is rather difficult to deploy on free hosting services.
2. Scraping does not works under some circumstances and hence the use of API would be better.
3. The requests are not made by different IP addresses (as my ProxyMesh trial has ended but you can use it).

To tackle the "1st" limitation I have tried deploying the server as a `Docker` container but it does not work, the issue lies with the `WebDriver` used by `selenium`.
