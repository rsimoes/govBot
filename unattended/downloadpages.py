import sys, os, re, subprocess, urllib, urllib2, MySQLdb, pdfminer, chardet, threading

def checkURL(url):
  try:
    code = urllib2.urlopen(url).code
  except:
    code = 404
  return code


def convertpdf(url):
  code = checkURL(url)
  if code >= 200 and code < 300:
    urllib.urlretrieve(url,'/tmp/temppdf.pdf')
    html = subprocess.call([sys.executable, '/usr/local/bin/pdf2txt.py', '-t', 'html', '/tmp/temppdf.pdf'])
    os.remove('/tmp/temppdf.pdf')
  else:
    html = code
  html = str(html)
  html = html.decode("ascii", "ignore")
  html = html.replace('\\','/')
  html = html.replace("'","\\'")
  html = html.replace('"','\\"')
  return html


def readhtml(url):
  try:
    response = urllib2.urlopen(url)
    code = response.code
    if code >= 200 and code < 300:
      html = response.read()
    else:
      html = code
  except:
      html = 'NULL'
  html = str(html)
  html = html.decode("ascii", "ignore")
  return html


class pageThread(threading.Thread):
  def __init__(self, threadID, name, counter, url):
    self.threadID = threadID
    self.name = name
    self.counter = counter
    self.url = url
  def run(self):
    print self.url


def downloadpages(limit = ''):
  limit = str(limit)
  query = 'SELECT id, url FROM url {0}'.format(limit).strip() + ';'

  db = MySQLdb.connect(host='173.255.254.42',db='fellowbot',read_default_file='~/.my.cnf')
  c = db.cursor()
  c.execute(query)
  urls = c.fetchall()
  urlcount = len(urls)
  position = 0
  
  for item in urls:
    print item
    url = str(item[1])
    urlid = int(item[0])
    
    if re.search('\.pdf',url):
      html = convertpdf(url)
    else:
      html = readhtml(url) 

    c.execute("""INSERT INTO html (source, collected_date, url_id) VALUES (%s, CURDATE(), %s);""", (html, urlid))
    db.commit()
  db.close()
  return len(list(urls))

def main():
  downloadpages('url is not null')

if __name__ == '__main__':
  main()
