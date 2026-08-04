import os
import psycopg2

url = os.environ.get('DATABASE_URL')
print('DATABASE_URL=', url)

try:
    conn = psycopg2.connect(url)
    print('connected')
    conn.close()
except Exception as e:
    print('error:', e)