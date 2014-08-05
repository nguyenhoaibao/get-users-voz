import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

#total url to parse
total_user = 10

#base url to parse
base_profile_url = 'http://vozforums.com/member.php?u=';

#host and port mongodb
host = 'localhost'
port = 27017

#proxy list
proxies = [
  '107.155.187.154:7808',
  '96.36.26.37:3128',
  '162.216.155.136:7808',
  '192.3.24.84:7808',
  '198.148.112.46:7808',
  '192.3.24.83:7808',
  '199.200.120.140:3127',
  '204.12.235.23:7808',
  '76.164.213.124:8089',
  '64.188.44.231:7808',
  '66.35.68.145:8089',
  '198.52.217.44:3127',
  '199.200.120.37:7808',
  '198.52.199.152:3127',
  '199.200.120.36:3127',
  '192.227.172.145:7808',
  '198.136.50.131:7808',
  '107.182.135.43:7808',
  '23.89.198.161:7808',
  '107.182.135.94:7808',
  '98.192.196.205:21320',
  '54.189.124.31:3128',
  '50.22.206.179:8080',
  '72.10.97.201:8080',
  '199.21.200.13:8081',
  '23.95.105.133:3128',
  '54.81.39.56:60884',
  '198.57.204.158:3128',
  '23.239.150.156:3128',
  '173.20.26.92:8080',
  '173.160.74.252:3128',
  '66.230.163.95:3128',
  '207.190.66.99:80',
  '207.223.117.198:3128',
  '54.72.33.20:80',
  '208.68.38.224:8080',
  '206.108.32.59:80',
  '216.164.218.251:8180',
  '192.3.171.92:80',
  '54.183.0.41:80',
  '50.200.88.218:7004',
  '68.120.91.23:21320',
  '24.247.171.212:21320',
  '75.144.114.189:8080',
  '174.136.39.121:8888',
  '172.245.25.41:8080',
  '54.215.190.162:80',
  '198.71.51.227:80',
  '23.236.48.43:8080',
  '97.122.162.70:3128',
  '70.179.142.180:21320',
  '96.42.37.122:21320',
  '72.227.82.123:21320',
  '70.189.225.112:21320',
  '24.94.58.72:21320',
  '76.254.5.187:21320',
  '173.175.149.118:21320',
  '98.186.171.88:21320',
  '50.95.34.177:21320',
  '24.143.103.93:21320'
]

proxy_dict = {}
timeout = 12

def get_mongo_connection():
  client = MongoClient(host, port)
  #select database
  db = client['user_voz']
  return db

def get_password():
  return 123456789;

def get_proxy():
  global proxy_dict
  proxy_dict = {
    "http" : "http://" + proxies.pop()
  }
  return proxy_dict

def get_parsed_html(profile_url):
  try:
    #if proxy is not set, set proxy
    global proxy_dict
    global timeout
    if not proxy_dict:
      proxy_dict = get_proxy()

    print "Use proxy: " + str(proxy_dict)
    r = requests.get(profile_url, proxies=proxy_dict, timeout=timeout)
  except requests.exceptions.Timeout:
    raise Exception("Timeout")
  except requests.exceptions.RequestException as e:
    raise Exception("Error", e.args)
  else:
    return r.text
  

def get_all_username():
  print "Get mongodb connection"
  mongo_db = get_mongo_connection()
  #select collection
  mongo_collection = mongo_db['user']
  for x in xrange(mongo_collection.find().count(), total_user):
    profile_url = base_profile_url + str(x)
    #html = urllib2.urlopen(profile_url)
    print "Parsing url: " + profile_url
    html = ''
    #try to parse html
    while not html:
      try:
        html = get_parsed_html(profile_url)
      except Exception as e:
        print "Error: " + str(e.args)
        #remove proxy cannot use
        global proxy_dict
        proxy_dict = {}
    
    #parse html
    try:
      parsed_html = BeautifulSoup(html)
      username = parsed_html.body.find('div', {'id' : 'main_userinfo'}).find('h1').text.strip()
      print "Username parsed: " + username
      mongo_collection.insert({'username' : username})
    except:
      print "Error occured"
      print "Pass user id: " + str(x)
      pass

def main():
  get_all_username();

if __name__ == '__main__':
  main()


#payload = {
#  'do'                      : 'login',
#  'api_cookieuser'          : 0,
#  'securitytoken'           : 'guest',
#  'api_vb_login_md5password': '7de8482cdbb8177365a8c5d4b53a74cd',
#  'api_vb_login_md5password_utf' : '7de8482cdbb8177365a8c5d4b53a74cd',
#  'api_vb_login_password'   : 'bao123456',
#  'api_vb_login_username'   : 'nguyenhoaibao',
#  'api_salt'                : 'LCGHW3JFY6KNEN5O'
#}

#s = requests.session()

#r = s.post('http://vozforums.com/vbdev/login_api.php', data=payload)
#print r.text.encode('utf-8')

#res = r.json()

#if res['captcha']:
#  payload['api_captcha'] = res['captcha'];
#  r = s.post('http://vozforums.com/vbdev/login_api.php', data=payload)
#  res = r.json()
#  if res['userinfo']['userid']:
#    r = s.get('http://vozforums.com');
#    with open('login_response.txt', 'w') as f:
#      f.write(r.text.encode('utf-8'))
