# Fujime
Fujime is a script that logs into Fujifilm's V.I.P program and notifies if the item you're looking for is in stock

Be careful with setting your Fuji V.I.P username/password as they will ban your IP if you've failed to login many times

Setting interval to 10 minutes is usually sufficient to get alerted when the items are in stock

## Config file

Modify config.yaml with your settings

- `fuji_username`: fuji vip program email
- `fuji_password`: fuji vip program password
- `urls`: list of names and urls you want to check for stock information
  - if you set email_notify to true, it will alert when either of these are in stock
- `check_every_seconds`: how often do you want to check the website for the stock info
- `email_notify`: if you want to alert you via email when the 
- `email_from` : from email that will be used to send emails
  - required if email_notify is set
- `email_to` : array of emails that the alerts will be send to. 
  - you can use email-to-sms provided by cell phone companies to send a text to your phone
  - required if email_notify is set
- `email_username`: email username to send email alerts as
- `email_password`: password for the email username
- `smtp_server`: smtp server that will be used to send emails
  - defaulted to Gmail. Can be any other mail server that supports TLS

## Running it in virtualenv

```
cd fujime
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python fujime.py --config config.yaml
```

## Running in docker container

### Build docker container
```
cd fujime
docker build -t fujime .
```

### Run docker container in foreground
```
docker run --name fujime fujime
```

### Run docker container in background, useful when "email_notify" is set
```
docker run -d --name fujime fujime
```

### Run docker and override config
If you've modified the config.yaml after you've built the container, you can override the config.yaml from your machine.
In this example, it's config.yaml in the current folder that would get exported into the docker container

```
docker run --name fujime -v `pwd`/config.yaml:/fujime/config.yaml fujime
```

### Run docker and browse around
```
docker run -it fujime /bin/bash
```

### Get inside an already running docker container
```
docker exec -it fujime /bin/bash
```

### View docker logs for the container
```
docker logs fujime
```

## Bugs

Right now the script only checks the first/default color of the item. For example if X100T is out of stock in Silver, but in stock for Black color, you will only get alerted when Silver goes on sale as it's the first/default one
