FROM python:3.6
COPY ./requirements.txt /tmp
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install -r /tmp/requirements.txt
ADD ./app /home/app
COPY ./entrypoint.sh /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh
#CMD ["/home/log-ingestion/manage.py run"]
ENTRYPOINT ["/home/app/entrypoint.sh"]
CMD []
