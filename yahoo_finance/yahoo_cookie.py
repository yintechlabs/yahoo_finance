import requests
import os
import yaml
import re
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

url = 'https://finance.yahoo.com/quote/SPY/history'
regex = '.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}'

cookieDir = os.path.expanduser('~')+'\cookieData'
if not os.path.exists(cookieDir):
    os.mkdir(cookieDir)
cookieFile = os.path.join(cookieDir,'yahoo_cookie.yml')
 
def getCookie():
    if not os.path.exists(cookieFile):
        setCookie()
    stream = open(cookieFile, 'r')
    dic = yaml.load(stream)
    return dic
 
def setCookie():
    r = requests.get(url)
    txt = r.text
    cookie = r.cookies['B']
    logging.debug('Cookie:', cookie)
    pattern = re.compile(regex)
    for line in txt.splitlines():
        m = pattern.match(line)
        if m is not None:
            crumb = m.groupdict()['crumb']
    logging.debug('Crumb= ', crumb)
    data = {'cookie':cookie,'crumb':crumb}
    with open(cookieFile,'w') as fid:
        yaml.dump(data,fid)
        
if __name__ == "__main__":
    cookieData = getCookie()
    print('Cookie= ', cookieData['cookie'])
    print(' Crumb= ', cookieData['crumb']) 