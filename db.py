import psycopg2

#Connecting to db
conn = psycopg2.connect(
    database = 'openbot',
    user = 'postgres',
    #password = '',
    #port = '5432',
    host = '127.0.0.1'  
)
print('\nDatabase connected successfully\n')

#Creating cursor
cur = conn.cursor()