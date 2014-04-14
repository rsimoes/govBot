SELECT table1.idoffices as idoffices, table1.officewordcount as officewords, table2.pagewordcount as pagewords, table2.pagewordcount < table1.officewordcount as missing
FROM (SELECT offices_has_words.offices_uid as idoffices, count(offices_has_words.words_idwords) as officewordcount
FROM offices_has_words
WHERE location = "official_name"
GROUP BY idoffices) as table1
LEFT JOIN (SELECT offices_has_pages.offices_uid as idoffices, count(pages_has_words.words_idwords) as pagewordcount
FROM offices_has_pages
INNER JOIN pages_has_words
ON offices_has_pages.pages_idpages = pages_has_words.pages_idpages
INNER JOIN offices_has_words
ON pages_has_words.words_idwords = offices_has_words.words_idwords
WHERE offices_has_pages.offices_uid = offices_has_words.offices_uid
AND offices_has_pages.page_types_idpage_types = 1
GROUP BY offices_has_pages.offices_uid) as table2
ON table1.idoffices = table2.idoffices;
