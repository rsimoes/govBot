import MySQLdb, re

def pullPages(cursor):
  query = '''SELECT person.name, html.source, person.id, officeholder.office_id, html.id
  FROM html
  INNER JOIN (SELECT max(collected_date) AS date, url_id
    FROM html
    GROUP BY url_id) AS recent
  ON recent.date = html.collected_date
  AND recent.url_id = html.url_id
  INNER JOIN officeholder
  ON source_url_id = html.id
  INNER JOIN person
  ON person_id = person.id;
  '''
  cursor.execute(query)
  pages = cursor.fetchall()
  return pages


def inspectPages(pages):
  confirmationList = []
  for item in pages:
    nameList = item[0].split(' ')
    page = item[1]
    confirmation = [item[4], item[2], item[3]]
    identifier = 0

    for name in nameList:
      pattern = re.compile(name.lower())
      if re.search(pattern, page.lower()):
        identifier += 1
    if identifier / len(nameList) == 1:
      confirmationList.append(confirmation)

  return confirmationList


def postConfirmations(confirmationList, cursor):
  for item in confirmationList:
    query = '''INSERT INTO confirmation
    (website_id, officeholder_person_id, officeholder_office_id)
    VALUES ({0}, {1}, {2});
    '''.format(item[0], item[1], item[2])
    cursor.execute(query)


def main():
  db = MySQLdb.connect(host='173.255.254.42',db='fellowbot',read_default_file='~/.my.cnf')
  cursor = db.cursor()

  postConfirmations(inspectPages(pullPages(cursor)), cursor)
  db.commit()


if __name__ == '__main__':
  main()