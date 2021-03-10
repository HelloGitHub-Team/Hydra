FROM python:3.9.1

WORKDIR /app
COPY . /app/

ENV HYDRA=online
ENV TIME_ZONE=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone

RUN pip install poetry==1.1.4 && poetry config virtualenvs.create false --local
RUN poetry install --no-root --no-dev

CMD [ "python", "-u", "run.py" ]