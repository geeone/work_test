import sqlite3 as lite
import requests
import urllib2
from threading import Thread

""" CHECK CONNECTION WITH SERVER """
def checkConnect():
    try:
        urllib2.urlopen('http://127.0.0.1:8000', timeout = 1)
    except urllib2.URLError:
        return False
    return True
"""
''' FUNCTION FOR MULTI-THREADING '''
def insertInside(ip, id, i):
    cur.execute('INSERT INTO Addresses (ID, IP, Source_ID, GUID) VALUES(NULL, "'+ip[i]+'", NULL, "'+id[i]+'")')
    con.commit()
    pass
"""
def insertToTable():
    for i in xrange(len(ip)):
        cur.execute('INSERT INTO Addresses (ID, IP, Source_ID, GUID) VALUES(NULL, "'+ip[i]+'", NULL, "'+id[i]+'")')
        con.commit()
    cur.execute('UPDATE Addresses SET Source_ID = (SELECT ID FROM Sources WHERE Name="'+ht+'")') 
    con.commit()
    """
    ''' MULTI-THREADING / DON'T WORK '''
    t = []
    for i in xrange(len(ip)):
        t.append(Thread(target=insertInside, args=(ip, id, i)))
        t[i].start()
    for i in xrange(len(ip)):
        t.join()
    """
    print "Operation is successfully completed."
    pass

if (checkConnect() != True):
    print "Error! Most likely, you forgot to run server."
else:
    """ SEND REQUEST TO SERVER """
    s = requests.session()
    print "Enter request type (http or socks): "
    tp = raw_input()
    r = s.get('http://127.0.0.1:8000/get_ip_list?type='+tp) #send request
    
    """ CHECK SERVER STATUS """
    if (r.status_code != 200):
        print "Error! Server isn't available. Status code - ", r.status_code
        pass
    else:
        """ GET HOST VALUE, IP & ID FROM SERVER """
        ct = r.content #get content
        hd = r.headers #get headers
        
        dct = {} #new dict
        dct = eval(ct) #convert string to dict
        d = dct.get('message') #get values from key 'message'
        
        dct1 = {}
        dct1 = eval(str(hd))
        ht = dct1.get('Host') #get values from key 'Host'
        
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
        
        #cur.execute('DROP TABLE Sources')
        #cur.execute('DROP TABLE Addresses')
        
        print "Please, wait..."
        cur.execute('SELECT * FROM Sources WHERE Name = "'+ht+'"')
        if (cur.fetchall() != []):
            print "This Host value has been got earlier."
        else:
            cur.execute('INSERT INTO Sources (ID, Name) VALUES(NULL, "'+ht+'")')
            con.commit()
        insertToTable()
        
        """" OUTPUT VALUES FROM TABLES """
        cur.execute('SELECT * FROM Sources')
        print cur.fetchall()
        cur.execute('SELECT * FROM Addresses')
        print cur.fetchall()
        con.close()

