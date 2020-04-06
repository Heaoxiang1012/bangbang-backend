import requests
url_params = {'muser':'041701407','passwd':'aoxiang1+2+3'}
url = 'http://59.77.226.32/logincheck.asp'
r = requests.post(url=url,params=url_params,allow_redirects=True)
print(r.history)