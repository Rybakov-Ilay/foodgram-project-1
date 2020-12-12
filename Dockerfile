FROM python:3.8.5
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt && chmod +x entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]