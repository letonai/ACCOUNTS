#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sqlite3
import os,time,re
import subprocess as sp
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


DATABASE="/home/pi/yowsup/dict.db"
TABLE="account"
class Account(object):

	def newAccount(self,uid):
		print "newAccount"
		CONN = sqlite3.connect("/home/pi/data/"+uid+".db")
		CURSOR = CONN.cursor()
		CURSOR.execute("create table "+TABLE+" (transid integer primary key AUTOINCREMENT,value real, balance real)")
		CURSOR.execute("insert into "+TABLE+" values (0,0,0)")
		CONN.commit()

	def getAccount(self,uid):
		if os.path.isfile("/home/pi/data/"+uid+".db"):
			CONN = sqlite3.connect("/home/pi/data/"+uid+".db")
			#CURSOR = CONN.cursor()
			return CONN
		else:
			return False

	def getBalance(self,uid):
		print "gtBalance"
		if not self.getAccount(uid):
                        self.newAccount(uid)
                conn = self.getAccount(uid)
		c=conn.execute('SELECT sum(value) FROM account')
		ret= str(c.fetchone()[0])
		c.close()
		return self.currencyFormat(ret)

	def doTransaction(self,value,uid):
		if not self.getAccount(uid):
			self.newAccount(uid)
		conn = self.getAccount(uid)
		#print str(conn.execute("SELECT max(transid) FROM "+TABLE).fetchone()[0])
		conn.execute("insert into "+TABLE+"(transid,value) values ((SELECT max(transid) FROM "+TABLE+")+1,'"+value+"')")
		conn.commit()

	def doCredit(self,value,uid):
		print "doCredit"
		value=value.rstrip("+")
		self.doTransaction(value,uid)

	def doDebit(self,value,uid):
		print "doDebit"
		value=value.rstrip("-")
		self.doTransaction("-"+value,uid)

	def getLastIssues(self,period):
		print "getLastIssue"
	
	def currencyFormat(self,value):
		return "R${0:.2f}".format(float(value))
