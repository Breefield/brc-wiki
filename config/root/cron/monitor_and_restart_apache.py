#!/usr/bin/env python
import pickle, os, sys, logging
from httplib import HTTPSConnection, socket
from smtplib import SMTP
import time
from subprocess import call

# url to monitor, hostname only
url = sys.argv[1]

def log(msg):
    import datetime
    timestamp = str(datetime.datetime.now())
    print timestamp, msg

def restart_services():
    log("Restarting services...")
    call(["/usr/sbin/service", "apache2", "stop"])
    call(["/usr/sbin/service", "varnish", "stop"])
    call(["/usr/sbin/service", "varnish", "start"])
    call(["/usr/sbin/service", "apache2", "start"])
    log("Services restarted.")

def get_site_status(url):
    response = get_response(url)
    try:
        if getattr(response, 'status') == 200:
            return 'up'
    except AttributeError:
    	pass
    return 'down'
        
def get_response(url):
    '''Return response object from URL'''
    try:
        conn = HTTPSConnection(url)
        conn.request('HEAD', '/')
        return conn.getresponse()
    except socket.error, e:
    	log(str(e))
        return None
    except Exception, e:
        log("Exiting")
        exit(1)

def is_running():
    f = open('/tmp/monitor_apache', 'w')
    f.write('')
    f.close()

def in_deploy():
    if os.path.exists('/srv/localwiki/.in_deploy'):
        if time.time() - os.path.getmtime('/srv/localwiki/.in_deploy') < (60*30):
            return True
        else:
            os.remove('/srv/localwiki/.in_deploy')
    return False 

if not is_running() and not in_deploy():
    if get_site_status(url) != 'up':
        log(url + " is down.")
        restart_services()
    else:
        log(url + " is up.")
    os.remove('/tmp/monitor_apache')
