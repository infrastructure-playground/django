FROM python:3.6.4
WORKDIR /usr/src/app
EXPOSE 8000

RUN apt-get update && \
    apt-get install vim -y

# COPY locale locale
# RUN python manage.py compilemessages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
