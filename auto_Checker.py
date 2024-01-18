import os
import requests
import psycopg2
import time
import logging
import functools
from main_scraper import main_Scraper
from database_manager import add_Laptop
from bs4 import BeautifulSoup


conn = psycopg2.connect(host = os.getenv('HOST'), database = os.getenv('DB'), user = os.getenv('NAME'), password = os.getenv('PASS'))
cursor = conn.cursor()

#CONFIGURING THE LOGGER
logg = logging.getLogger('checker')
logg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file = logging.FileHandler('checker-logs.logs')
file.setFormatter(formatter)
stream = logging.StreamHandler()
stream.setFormatter(formatter)
stream.setLevel(logging.INFO)
logg.addHandler(file)
logg.addHandler(stream)

def timer(func):
    '''CONFIGURE THE TIME IN add_Timer FUNCTION'''
    @functools.wraps(func)
    def add_Timer():
        time.sleep(7200) # < - - Change the wait time here
        return func()
    return add_Timer

@timer
def main_Checker():
    params = {'page' : 1}
    url = 'https://www.dell.com/en-us/shop/dell-laptops/sr/laptops/xps?appliedRefinements=37868,37873,37869,37867,37865'
    headers = {os.getenv('AGENT') : os.getenv('DATA')}
    req = requests.get(url, params = params, headers = headers)
    new_laptop_list = main_Scraper(req)
    cursor.execute('SELECT model, current_price, processor, os, graphics, memory, storage, display FROM laptop_data')
    new_counter = 0
    laptops = cursor.fetchall()
    
    if len(new_laptop_list) < len(laptops):
        logg.info('{} laptops were deleted...'.format(len(laptops) - len(new_laptop_list)))
    else:
        for laptop in new_laptop_list:
            data = []
            for i in laptop:
                data.append(i[-1])
            if tuple(data) not in laptops:
                new_counter += 1
                #add_Laptop(laptop)
        if new_counter > 0:
            logg.info('{}  laptops were added/modified.  Succesfully added them to the database!'.format(new_counter))
        else:
            logg.info('There were no new laptops added on the website..')

    
  
while(True):
    main_Checker()


conn.commit()
conn.close()
cursor.close()
