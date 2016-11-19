#!/usr/bin/python

import MySQLdb
from datetime import date
import sys
from settings import *

default_prio = 14400

def get_soa_for_domain(domainname):
	db = MySQLdb.connect(host=sqlhost,user=sqluser, passwd=sqlpwd,db=sqldb)
	print 'trying to get SOA for domain={0}'.format(domainname)
        crs=db.cursor(MySQLdb.cursors.DictCursor)
        crs.execute("""SELECT id FROM domains WHERE name = %s""", (domainname,))
        if crs.rowcount > 0:
                row = crs.fetchone()
                domain_id = row["id"]
                print "domain {0} gevonden in db, domain id={1}".format(domainname, domain_id)
		print "trying to get SOA-record"
        	crs.execute("""SELECT content FROM records WHERE domain_id = %s and type ='SOA'""", (domain_id,))
        	if crs.rowcount > 0:
                	row = crs.fetchone()
			print "SOA for domain {0} = {1}".format(domainname, row["content"])
                        old_soa = row['content'].split()
                        # generate new SOA serial:
                        # if soa date is today
                        if old_soa[2][:8] == date.today().strftime("%Y%m%d"):
                                old_soa[2] = str(int(old_soa[2]) + 1)
				# todo: what todo if SOA-serial > 99?
                        else:
                                old_soa[2] = date.today().strftime("%Y%m%d") + '00'
                        new_soa = ' '.join(old_soa)
                        # updaten SOA
                        crs.execute("""UPDATE records SET content = %s WHERE domain_id = %s AND type ='SOA'""", (new_soa,domain_id,))
                        print "succesfully updated domain: {0}".format(domainname)
			db.commit()
		else:
			print "no SOA record found for domain {0}".format(domainname)
	else:
		print "the given domain is not found in db"

        db.close()

# let op in argv[0] zit altijd de naam van het script zelf
if len(sys.argv) > 1:
	get_soa_for_domain(sys.argv[1])
else:
	print "Not enough arguments\nExample usage:\nupdate_soa.py <domainname>\n"


def process_domain_name_list():
	domain_name_list_file  = './update_soa.txt'
	domain_name_list = [line.rstrip('\n') for line in open(domain_name_list_file)]
	for domain_name in domain_name_list:
		print "processing domain {0}".format(domain_name)
		try:
			get_soa_for_domain(domain_name)
		except:
			print 'fout lezen domain name list'
