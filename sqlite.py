import sqlite3 as lite
import requests
import urllib2
from threading import Thread
from threading import BoundedSemaphore

""" CHECK CONNECTION WITH SERVER """
def checkConnect():
    try:
        urllib2.urlopen('http://127.0.0.1:8000', timeout = 1)
    except urllib2.URLError:
        return False
    return True

def insertToTable():
    for i in xrange(len(ip)):
        cur.execute('INSERT INTO Addresses (ID, IP, Source_ID, GUID) VALUES(NULL, "'+ip[i]+'", NULL, "'+id[i]+'")')
        con.commit()
    print "Operation is successfully completed."
    pass

if (checkConnect() != True):
    print "Error! Most likely, you forgot to run the server."
else:
    """ SEND REQUEST TO SERVER """
    s = requests.session()
    r = s.get('http://127.0.0.1:8000/get_ip_list?type=http') #send request
    
    """ CHECK SERVER STATUS """
    if (r.status_code != 200):
        print "Error! Server isn't available. Status code - ", r.status_code
        pass
    else:
        """ GET IP & ID FROM SERVER """
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
        
        #cur.execute('DROP TABLE Addresses')
        
        print "Please, wait..."
        insertToTable()
        
        cur.execute('SELECT * FROM Sources')
        print cur.fetchall()
        cur.execute('SELECT * FROM Addresses')
        print cur.fetchall()
        con.close()

