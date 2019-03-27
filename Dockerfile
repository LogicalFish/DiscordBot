FROM python:3-alpine

RUN apk add --no-cache --virtual .build-deps \
            gcc \
            libc-dev \
            libffi-dev \
            make

RUN pip install --upgrade discord.py python-dateutil \
 && python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/async.zip#egg=discord.py[voice] \
 && pip install --upgrade aiohttp websockets emoji \
 && pip install --upgrade psycopg2-binary

ENV GID 10000
ENV UID 10000

RUN addgroup -g ${GID} app && adduser -u ${UID} -G app -D -H app

ENV APP_ROOT /var/run/app/

RUN mkdir -p ${APP_ROOT}  \
 && chown ${GID}:${UID} ${APP_ROOT}
WORKDIR ${APP_ROOT}

USER app

COPY python ${APP_ROOT}

CMD ["python", "main.py"]