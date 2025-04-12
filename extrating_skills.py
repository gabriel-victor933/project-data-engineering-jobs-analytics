"""
Extrair as skills desejadas e os nivels de experiência com a respectiva descrição.
"""
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import time
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

USERNAME = os.getenv('POSTGRES_USERNAME')
PASSWORD = os.getenv('POSTGRES_PASSWORD')

def extract_text_from_dropdown(elems, remove_first=True):
    arr = []
    for elem in elems:
        arr.append(elem.text)

    if remove_first:
        arr.pop(0)

    return arr

URL = 'https://www.99freelas.com.br/projects?categoria=web-mobile-e-software&data-da-publicacao=menos-de-3-dias-atras'

URL_TEMP = 'https://www.99freelas.com.br/project/new'

options = options = webdriver.ChromeOptions()
options.timeouts = { 'implicit': 5000 } # Espera de 5s na localizacao de elemento
options.add_argument("--start-maximized")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get(URL_TEMP)

element_skills = driver.find_element(By.CLASS_NAME,'itens-to-select')

full_text = element_skills.text

skills = full_text.split('\n')

element_exp = driver.find_element(By.CLASS_NAME,'list-group')

exp = element_exp.text.split('\n')

dict_exp = {
    'level': [],
    'description': []
}
for i in range(0,len(exp),2):
    dict_exp['level'].append(exp[i])
    dict_exp['description'].append(exp[i+1])

element_cat = driver.find_element(By.ID,'categoria')

elements_cat = element_cat.find_elements(By.TAG_NAME,'option')

categories = extract_text_from_dropdown(elements_cat)

dict_subcat = {}
for elem in elements_cat[1:]:
    elem.click()

    cat_number = elem.get_attribute('value')

    if cat_number == '10':
        continue

    elem_subcat = driver.find_element(By.ID, f'subcategoria-{cat_number}')

    elems_subcat = elem_subcat.find_elements(By.TAG_NAME,'option')
    
    dict_subcat[elem.text] = extract_text_from_dropdown(elems_subcat)


# TODO: inserir experience_level no DB

# TODO: Inserir categorias no db

# TODO: inserir subcategorias

# TODO: inserir skills

time.sleep(1)

driver.quit()