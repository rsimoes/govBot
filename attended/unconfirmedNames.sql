SELECT district.electoral_district AS district, office.office_name AS office_name, person.name AS name, url.url AS url
FROM officeholder 
LEFT OUTER JOIN confirmation 
ON officeholder_office_id = office_id 
AND officeholder_person_id = person_id
INNER JOIN person
ON officeholder.person_id = person.id
INNER JOIN url
ON officeholder.source_url_id = url.id
INNER JOIN office
ON officeholder.office_id = office.id
INNER JOIN district
ON district_id = district.id
WHERE confirmation.website_id is NULL;