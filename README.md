# coffee_shop

######database 
#backup
ali
mysqldump -h localhost -P 3306 -u root -p <passwd> --databases <databasename> > /tmp/test.sql

output test.sql

#recover
ali
docker cp /tmp/test.sql <containerid> :/tmp/test.sql
docker exec -it <containerid> bash
mysql -u root -p <passwd>
source /tmp/test.sql


