import psycopg2

#connection to database
conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")

#cursor
c=conn.cursor()

#Query test1
c.execute('SELECT * FROM test1;')
print(c.fetchall())

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS *** (columns TYPE)''')
    conn.commit()

def insert_data():
    c.execute("INSERT INTO *** (columns) VALUES (?, ?);", data)
    conn.commit()

def select_all():
    pass

