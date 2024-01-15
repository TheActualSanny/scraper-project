import psycopg2
import os
from dotenv import load_dotenv
from mainscraper import Laptop, laptop_list

conn = psycopg2.connect(host = os.getenv('HOST'), database = os.getenv('DB'), user = os.getenv('NAME'), password = os.getenv('PASS'))
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS laptop_data(id integer PRIMARY KEY,
model text,
current_price real,
processor test,
os text,
graphics text,
memory text,
storage text,
display text
)""")

index = 1
for laptop in laptop_list:
    with conn:
        cursor.execute('''
            INSERT INTO laptop_data(id, model, current_price, processor, os, graphics, memory, storage, display)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            index
            laptop.model,
            laptop.curr_price,
            laptop.processor,
            laptop.os,
            laptop.graphics,
            laptop.memory,
            laptop.storage
            laptop.display
        ))
    index += 1
    
conn.commit()
conn.close()
cursor.close()
