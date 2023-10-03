# import psycopg2

# conn = psycopg2.connect(dbname="soumi_postgres",
#                         user="soumi_postgres_user",
#                         host="dpg-ckd4dmect0pc73de3sb0-a.oregon-postgres.render.com",
#                         password="IGTWm8MArz5Eix3WihNEXqIWmccu10sd",
#                         port="5432")
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM information_schema.tables')
# rows = cursor.fetchall()
# for table in rows:
#     print(table)
# conn.close()