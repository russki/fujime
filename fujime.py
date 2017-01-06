import cookielib 
import urllib2 
import mechanize 
import re
import time
import smtplib
import pprint
import yaml
import logging
import sys
import argparse

from os import path
from bs4 import BeautifulSoup

SUBJECT="Great news! Fuji is available"
NOTIFY_TEMPLATE = "Name: {0} Url: {1} Price: ${2} Availability: {3}"

pp = pprint.PrettyPrinter(indent=4)

# Browser 
br = mechanize.Browser() 

# Enable cookie support for urllib2 
cookiejar = cookielib.LWPCookieJar() 
br.set_cookiejar( cookiejar ) 

# Broser options 
br.set_handle_equiv( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 

br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 10 ) 

br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.13 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.13' ) ] 

def main(settings):
  urls = settings.get('urls')
  sleep = settings.get('check_every_seconds', 60)
  fromaddr = settings.get('email_from')
  toaddrs  = settings.get('email_to')
  email_username = settings.get('email_username')
  email_password = settings.get('email_password')
  smtp_server = settings.get('smtp_server')
  fuji_username = settings.get('fuji_username')
  fuji_password = settings.get('fuji_password')
  email_notify = settings.get('email_notify')

  while True:
    email_message = ""
    # authenticate 
    br.open('http://fnacaffiliate.com/v.i.p/index.php?dispatch=auth.login_form&return_url=index.php%3Fdispatch%3Dproducts.view%26product_id%3D362') 
    br.select_form( name="popup886_form" ) 
    br[ "user_login" ] = fuji_username
    br[ "password" ] = fuji_password
    res = br.submit() 
  
    for name, url in urls.iteritems():
      response = br.open(url)
      soup = BeautifulSoup(response.read(), 'html.parser')
      avail = soup.findAll("span", id=re.compile('.*stock_info.*'))
      price = soup.find("meta", {"itemprop":"price"})
      item_info = NOTIFY_TEMPLATE.format(name, url, price['content'], avail[0].contents[0])
      if avail[0].contents[0]=='In stock':
        logging.info('%s' % item_info)
        email_message += item_info + "\n"
      time.sleep(1)

    if email_notify == True and email_message != "":
      msg = 'Subject: {0}\n\n{1}'.format(SUBJECT,email_message)
      server = smtplib.SMTP(smtp_server)
      server.starttls()
      server.login(email_username,email_password)
      server.sendmail(fromaddr, toaddrs, msg)
      server.quit()

    logout='http://fnacaffiliate.com/v.i.p/index.php?dispatch=auth.logout&redirect_url=index.php'
    response = br.open(logout)
    time.sleep(sleep)

def _check_settings(config):
  required_settings = (
    'fuji_username',
    'fuji_password'
  )

  for setting in required_settings:
    if not config.get(setting):
      raise ValueError('Missing setting "%s" in config.yaml file.' % setting)

  if config.get('email_notify') == True:
    if not config.get('email_from') or not config.get('email_to'):
      raise ValueError('email_to and email_from are required for sending email. Set email_notify to false to disable mail')
    if not config.get('email_username') or not config.get('email_password'):
      raise ValueError('email_username and email_password are required for sending email. Set email_notify to false to disable mail')

if __name__ == '__main__': 
  # Configure Basic Logging
  logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    stream=sys.stdout,
  )

  # Parse Arguments
  parser = argparse.ArgumentParser(description="Script to check for Fuji availability")
  parser.add_argument('--config', dest='configfile', default='config.yaml', help='Config file to use (default is config.yaml)')
  arguments = vars(parser.parse_args())

  # Load Settings
  try:
    with open(arguments['configfile']) as yaml_file:
      settings = yaml.load(yaml_file)
      _check_settings(settings)
  except Exception as e:
    logging.error('Error loading settings from config.yaml file: %s' % e)
    sys.exit()

  # Configure File Logging
  if settings.get('logfile'):
    handler = logging.FileHandler('%s/%s' % (pwd, settings.get('logfile')))
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    handler.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(handler)

  logging.debug('Running Fujime with arguments: %s' % arguments)
  main(settings)
