#create a dump of the DB example
mysqldump example > dump.sql

#create a DB sample and copy the data from the DB example there
mysqladmin create sample | mysql sample < dump.sql