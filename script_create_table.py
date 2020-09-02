import psycopg2

#connection to database
conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")

#cursor
curs=conn.cursor()

#Query test1
curs.execute('SELECT * FROM test1;')
print(curs.fetchall())

def create_table():
    pass

def insert_data():
    pass

def select_all():
    pass

