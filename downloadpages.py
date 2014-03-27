import sys, os, re, subprocess, urllib, urllib2, MySQLdb, pdfminer, chardet

def checkURL(url):
  code = urllib2.urlopen(url).code 
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
  html = html.replace('\\','/')
  html = html.replace("'","\\'")
  html = html.replace('"','\\"')
  return html

def downloadpages(limit = 'current_source is null', original = False):
  ##Limit is a string which is used as the 'WHERE' clause of a query against the pages table (Excluding the word 'WHERE')
  ##Original is a boolean which indicates whether the html should be stored in the 'original_source' column. When False, html will be stored in current_source
  limit = str(limit)
  if len(limit) > 0:
    query = 'SELECT DISTINCT url FROM pages WHERE '+limit+';'
  else:
    query = 'SELECT DISTINCT url FROM pages;'
  if original:
    col1 = 'original_source'
    col2 = 'created_date'
  else:
    col1 = 'current_source'
    col2 = 'updated_date'
  db = MySQLdb.connect(host='173.255.254.42',db='fellowbot',read_default_file='~/.my.cnf')
  c = db.cursor()
  c.execute(query)
  urls = c.fetchall()
  for item in urls:
    url = str(item[0])
    print item
    if re.search('\.pdf',url):
      html = convertpdf(url)
    else:
      html = readhtml(url) 
    query = "UPDATE pages SET {0}='{1}', {2}=CURDATE() WHERE url='{3}';\n\n".format(col1, html, col2, url.replace('\'',"\\'")) 
    c.execute(query)
    db.commit()
  db.close()
  return len(list(urls))

downloadpages()
