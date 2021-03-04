FROM python:3.9.1

WORKDIR /app
ADD . /app/

ENV HYDRA=online
ENV TIME_ZONE=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone

RUN pip install poetry && poetry config virtualenvs.create false --local
RUN poetry install --no-root --no-dev

CMD [ "python", "./run.py" ]