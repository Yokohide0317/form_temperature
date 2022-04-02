FROM python:3.7-slim-buster

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    oathtool \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install autopep8 selenium pyotp

ARG _URL="https://forms.office.com/Pages/ResponsePage.aspx?id=XYP-cpVeEkWK4KezivJfyCeFAslPic5ClvPV53svxD1UMERBS0pEU0xGNlUzMlpCQkNYODZSREhVWS4u"
ARG _EMAIL=""
ARG _PASSWORD=""
ARG _AUTH_KEY=""

ENV URL ${_URL}
ENV EMAIL ${_EMAIL}
ENV PASSWORD ${_PASSWORD}
ENV AUTH_KEY ${_AUTH_KEY}
