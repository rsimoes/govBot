import MySQLdb
def wordsfromoffices(limit):
  
  db = MySQLdb.connect(host='173.255.254.42', db='fellowbot',read_default_file='~/.my.cnf')
  c = db.cursor()
  if len(limit) > 0:
    query = 'select uid, office_name, official_name, official_party from offices {0};'.format(limit)
  else:
    query = 'select uid, office_name, official_name, official_party from offices;'
  c.execute(query)
  officeinfo = c.fetchall()

  word = []
  location = []
  ids = []
  locations = ['office_name', 'official_name', 'official_party']
  for item in officeinfo:
    print item
    for i in range(3):
      words = item[i+1].lower().replace(","," ").replace("'","\\'").replace("-"," ").replace("   "," ").replace("  "," ").split(" ")
      for element in words:
        idquery = "select idwords from words where word = '{0}';".format(element)
        insertword = "insert into words (word) values ('{0}');".format(element)
        result = c.execute(idquery)
        if result > 0:
          wordid = c.fetchone()[0]
          checkexists = "select * from offices_has_words where offices_uid = '{0}' and words_idwords ='{1}';".format(item[0],wordid)
          test = c.execute(checkexists)
          if test > 0:
            continue
        else:
          c.execute(insertword)
          db.commit()
          c.execute(idquery)
          wordid = c.fetchone()[0] 
        insertrelationship ="insert into offices_has_words (offices_uid, words_idwords, location) values ('{0}', '{1}', '{2}');".format(item[0], wordid, locations[i])
        c.execute(insertrelationship)
        db.commit()
  db.close()

wordsfromoffices('left outer join offices_has_words on uid=offices_uid where offices_uid is NULL')
