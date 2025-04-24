from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import os
import psycopg2 # type: ignore
from itertools import product
from dotenv import load_dotenv # type: ignore
 
load_dotenv()

USERNAME = os.environ['POSTGRES_USERNAME']
PASSWORD = os.environ['POSTGRES_PASSWORD']
DB = os.environ['POSTGRES_DATABASE']
HOST = os.environ['POSTGRES_HOST']
PORT = os.environ['POSTGRES_PORT']
URL = os.environ['URL_SKILLS']

def get_webdriver(url, headless=True):
    options = options = webdriver.ChromeOptions()
    options.timeouts = { 'implicit': 5000 } # Espera de 5s na localizacao de elemento
    options.add_argument("--start-maximized")
    options.add_argument("--headless")              # modo sem GUI
    options.add_argument("--no-sandbox")            # necessário no container
    options.add_argument("--disable-dev-shm-usage") # evita falta de memória compartilhada

    if headless:
        options.add_argument("--headless")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    

    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    driver.get(url)

    return driver


def get_db_connnection():
    return psycopg2.connect(dbname=DB, user=USERNAME, password=PASSWORD, host=HOST, port=PORT)


def load_references():
    conn = get_db_connnection()

    cur = conn.cursor()

    cur.execute('SELECT id, level FROM experience_levels;')
    levels = cur.fetchall()

    cur.execute('SELECT id, subtype FROM subcategories;')
    subcategories = cur.fetchall()

    conn.close()

    return levels, subcategories
    
def return_id(arr, item):
    for number in arr:
        if number[1] == item:
            return number[0]

def save_jobs(jobs):

    conn = get_db_connnection()

    cur = conn.cursor()

    levels, subcategories = load_references()

    for job in jobs:
        job['experience_level'] = return_id(levels,job['experience_level'])
        job['subcategory'] = return_id(subcategories,job['subcategory'])

        skills = None
        if 'skills' in job:
            skills = job['skills']
            del job['skills']

        try:
            cur.execute("""
                INSERT INTO jobs 
                (level_id, subcategory_id, title, description, publication_date, limit_date,extraction_date)
                VALUES (%(experience_level)s, %(subcategory)s, %(title)s, %(description)s, %(publication_date)s, %(limit_date)s, %(extraction_date)s)
                RETURNING id
            """
            ,job)

            job_id = cur.fetchone()

            if skills is not None:
                placeholders = ','.join(['%s'] * len(skills))
                cur.execute(f'SELECT id FROM skills WHERE name IN ({placeholders})',skills)
                skills_id = [id for (id,) in cur.fetchall()]
                

                jobs_skills = list(product(job_id,skills_id))

                cur.executemany('INSERT INTO jobs_skills (job_id, skill_id) VALUES (%s, %s)',jobs_skills)

            print('job posted')
        except Exception as e:
            print(f'Error at upload of {job["title"]}')
            print(e)

        finally:
            conn.commit()  

