#!/usr/bin/python

import MySQLdb
from datetime import date
import sys
import settings

default_prio = 14400

def get_soa_for_domain(domainname):
	db = MySQLdb.connect(host=sqlhost,user=sqluser, passwd=sqlpwd,db=sqldb)
	print 'trying to get SOA for domain={0}'.format(domainname)
        crs=db.cursor(MySQLdb.cursors.DictCursor)
        crs.execute("""SELECT id FROM domains WHERE name = %s""", (domainname,))
        if crs.rowcount > 0:
                row = crs.fetchone()
                domain_id = row["id"]
                print "domain {0} gevonden in db, domein id={1}".format(domainname, domain_id)
		print "trying to get SOA-record"
        	crs.execute("""SELECT content FROM records WHERE domain_id = %s and type ='SOA'""", (domain_id,))
        	if crs.rowcount > 0:
                	row = crs.fetchone()
			print "SOA for domain {0} = {1}".format(domainname, row["content"])
		else:
			print "no SOA record found for domain {0}".format(domainname)
	else:
		print "the given domain is not found in db"

	#new_soa = ' '.join(old_soa)
	# updaten SOA
	#crs.execute("""UPDATE records SET content = %s WHERE domain_id = %s AND type ='SOA'""", (new_soa,domain_id,))
	#print "succesfully updated domein: {0}".format(domainname)
	#print "nr of sql_actions voor domein {0} = {1}".format(domainname, sql_actions)

        print "\n"
	#        db.commit()
        db.close()

# let op in argv[0] zit altijd de naam van het script zelf
if len(sys.argv) > 1:
	get_soa_for_domain(sys.argv[1])
else:
	print "Not enough arguments\nExample usage:\nupdate_soa.py <domainname>\n"
