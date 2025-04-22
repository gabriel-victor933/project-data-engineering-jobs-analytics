from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import time
import os
import psycopg2 # type: ignore
from psycopg2.extras import execute_batch # type: ignore
from dotenv import load_dotenv # type: ignore
from tools import get_webdriver, save_jobs
import datetime
from utils import clean_string
import json


print('initiating extraction!')
load_dotenv()

URL = os.environ['URL_JOBS']
print(f'teste: {URL}')
driver = get_webdriver(f'{URL}&data-da-publicacao=menos-de-3-dias-atras',headless=True)

results_header = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/p')
total_pages = int(results_header.text.split(' ').pop(0))//10 + 1

current_page = 1

driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/span').click()

time.sleep(1)

now = datetime.datetime.now()

for i in range(1,total_pages + 1):
    try:
        driver.get(f'{URL}order=mais-antigos&data-da-publicacao=menos-de-3-dias-atras&page={i}')
    
        time.sleep(1)
        jobs_list = []
        ## Get all jobs in page:
        jobs_lu_elem = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[3]/ul')
        jobs = jobs_lu_elem.find_elements(By.TAG_NAME,'li')

        ## job == li
        for job in jobs:
            job_dict = {}

            job_header = job.find_element(By.TAG_NAME,'hgroup')

            job_dict['title'] = job_header.find_element(By.TAG_NAME,'h1').text

            description_tag = job.find_element(By.CSS_SELECTOR,'div.description')

            #try to expand
            try:
                spans = description_tag.find_elements(By.TAG_NAME,'span')
                if len(spans) > 0:
                    spans[0].find_element(By.TAG_NAME,'a').click()
                    
            except Exception as e:
                print(e)
                print('error at expading description')

            time.sleep(1)

            description = description_tag.text.replace(' Esconder', '')
            job_dict['description'] = clean_string(description)

            information_tag = job_header.find_element(By.CSS_SELECTOR,'p.information')

            information_text = information_tag.text

            sub_category, level, _ = information_text.split('|', maxsplit=2)

            job_dict['subcategory'] = sub_category.strip()
            job_dict['experience_level'] = level.strip()

            date_timestamp = job_header.find_element(By.CSS_SELECTOR,'b.datetime').get_attribute('cp-datetime')
            date_timestamp = int(date_timestamp)
            posting_date = datetime.datetime.fromtimestamp(date_timestamp/1000).isoformat()

            dateleft_timestamp = job_header.find_element(By.CSS_SELECTOR,'b.datetime-restante').get_attribute('cp-datetime')
            dateleft_timestamp = int(dateleft_timestamp)
            limit_date = datetime.datetime.fromtimestamp(dateleft_timestamp/1000).isoformat()

            job_dict['publication_date'] = posting_date
            job_dict['limit_date'] = limit_date

            job_dict['extraction_date'] = now.isoformat()

            # get skills
            try:
                skills_elem = job.find_elements(By.CSS_SELECTOR, 'p.habilidades a.habilidade')
                if len(skills_elem) > 0:
                    job_dict['skills'] = []
                    for skill in skills_elem:
                        job_dict['skills'].append(skill.text)

            except Exception as e:
                print('Error at extracting job skills')

            jobs_list.append(job_dict)

        #remover comentario depois
        #save_jobs(jobs_list)        

        print(jobs_list)

        break
        
    except Exception as e:
        print(f'Não foi possivel extrair dados da página {i}')
        print(e)
    

driver.quit()

