import psycopg2
import os
from dotenv import load_dotenv
from main_scraper import Laptop, laptop_list

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

index = len(laptop_list)

def add_Laptop(inst):
    global index 
    with conn:
        cursor.execute('''INSERT INTO laptop_data(id, model, current_price, processor, os, graphics, memory, storage, display)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (index, inst.model, inst.curr_price, inst.processor, inst.os, inst.graphics, inst.memory, inst.storage, inst.display))
    index += 1

def del_Laptop(ind):
    global index
    with conn:
        cursor.execute('DELETE FROM laptop_data WHERE id = %s', (ind,))
    index -= 1

def find_Laptop(price_min, price_end):
    cursor.execute('SELECT * FROM laptop_data WHERE current_price > %s AND current_price < %s', (price_min, price_end))
    return cursor.fetchall()
    
create_index = 1
for laptop in laptop_list:
    with conn:
        cursor.execute('''
            INSERT INTO laptop_data(id, model, current_price, processor, os, graphics, memory, storage, display)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            create_index
            laptop.model,
            laptop.curr_price,
            laptop.processor,
            laptop.os,
            laptop.graphics,
            laptop.memory,
            laptop.storage
            laptop.display
        ))
    create_index += 1
    
conn.commit()
conn.close()
cursor.close()
