FROM python:3.8.5
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install -r requirements.txt && chmod +x entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]