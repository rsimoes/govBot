import MySQLdb, re

def checkpagesforwords(limit):
  db = MySQLdb.connect(host='173.255.254.42',db='fellowbot',read_default_file='~/.my.cnf')
  pagecursor = db.cursor()
  count = pagecursor.execute("""
    select offices_has_words.offices_uid, words.word, pages.original_source, words.idwords, pages.idpages
    from offices_has_words
    inner join words on words_idwords=idwords
    inner join offices_has_pages on offices_has_pages.offices_uid = offices_has_words.offices_uid
    inner join pages on idpages = pages_idpages
    {0};""".format(limit))
  updatecursor = db.cursor()
  ##Proceed one word instance at a time, search for words in the related source, update pages_has_words
  ##ERROR: Inserting duplicate rows
  for i in range(count):
    item = pagecursor.fetchone()
    print item[0]
    if re.search(str(item[1]).replace('\.','\\\.'),str(item[2]).lower().replace(","," ").replace("-"," ")):
      if updatecursor.execute("select * from pages_has_words where pages_idpages = {0} and words_idwords = {1} and location = 'source';".format(item[4], item[3])) == 0:
        updatecursor.execute("insert into pages_has_words (pages_idpages, words_idwords, location) values ('{0}', '{1}', 'source');".format(item[4], item[3]))
        db.commit()
  
  db.close()

checkpagesforwords("where offices_has_words.location = 'official_name' and offices_has_pages.page_types_idpage_types = 1")
