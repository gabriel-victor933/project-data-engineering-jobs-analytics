from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import psycopg2 # type: ignore

load_dotenv()

USERNAME = os.getenv('POSTGRES_USERNAME')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DATABASE')
HOST = os.getenv('POSTGRES_HOST')
PORT = os.getenv('POSTGRES_PORT')
URL = os.getenv('URL_SKILLS')

def get_webdriver(url, headless=True):
    options = options = webdriver.ChromeOptions()
    options.timeouts = { 'implicit': 5000 } # Espera de 5s na localizacao de elemento
    options.add_argument("--start-maximized")

    if headless:
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    return driver


def get_db_connnection():
    return psycopg2.connect(dbname=DB, user=USERNAME, password=PASSWORD, host=HOST, port=PORT)