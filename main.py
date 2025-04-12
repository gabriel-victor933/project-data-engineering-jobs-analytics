from bs4 import BeautifulSoup # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import time

URL = 'https://www.99freelas.com.br/projects?categoria=web-mobile-e-software&data-da-publicacao=menos-de-3-dias-atras'

URL_TEMP = 'https://www.99freelas.com.br/project/new'

options = options = webdriver.ChromeOptions()
options.timeouts = { 'implicit': 5000 } # Espera de 5s na localizacao de elemento
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

driver.get(URL_TEMP)

time.sleep(600)

driver.quit()