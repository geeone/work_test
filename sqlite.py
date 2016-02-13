import sqlite3 as lite
import requests

""" GET IP & ID FROM SERVER """
s = requests.session()
r = s.get('http://127.0.0.1:8000/get_ip_list?type=http') #send request
str = r.content #get text

dct = {} #new dict
dct = eval(str) #convert string to dict
d = dct.get('message') #get values from key 'message'

ip = [] #new lists
id = []

for i in xrange(len(d)):
    ip.append(d[i].get('ip')) #get values from key 'ip' to new list'ip'
    id.append(d[i].get('id')) #get values from key 'id' to new list'id'

""" CREATE DATABASE & INSERT VALUES TO TABLES """
con = None
con = lite.connect('test.db')
cur = con.cursor()    

try:
    cur.execute('CREATE TABLE Sources (ID INTEGER PRIMARY KEY, Name VARCHAR(100))')
except lite.DatabaseError, x:
    print "Error: ", x
con.commit()
try:
    cur.execute('CREATE TABLE Addresses (ID INTEGER PRIMARY KEY, IP VARCHAR(100), Source_ID INTEGER, GUID VARCHAR(100))')
except lite.DatabaseError, x:
    print "Error: ", x
con.commit()

for i in xrange(len(ip)):
    cur.execute('INSERT INTO Addresses (ID, IP, Source_ID, GUID) VALUES(NULL, "'+ip[i]+'", NULL, "'+id[i]+'")')
    con.commit()

cur.execute('SELECT * FROM Addresses')
print cur.fetchall()
con.close()
