import psycopg2
import os
from dotenv import load_dotenv
psycopg2.connect()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS laptop_data(id integer PRIMARY KEY,
model text,
current_price real,
processor test,
os text,
praphics text,
memory text,
storage text,
display text
)""")
import psycopg2
from main_scraper import Laptop, laptop_list

conn = psycopg2.connect(
    database="your_database",
    user="your_user",
    password="your_password",
    host="your_host",
    port="your_port"
)

for laptop in laptop_list:
    with conn:
        cursor.execute('''
            INSERT INTO laptops (model, curr_price, processor, os, graphics, memory, storage)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            laptop.model,
            laptop.curr_price,
            laptop.processor,
            laptop.os,
            laptop.graphics,
            laptop.memory,
            laptop.storage
        ))
conn.commit()
conn.close()
cursor.close()
