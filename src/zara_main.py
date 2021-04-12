from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dataset_data import *
import pandas as pd

dataset_headers = ['id', 'group', 'category', 'images', 'size', 'colour', 'season', 'price', 'made_in', 'clothes_care', 'brand']
data_dict = {'id':[], 'group':[], 'category':[], 'images':[], 'size':[], 'colour':[], 'season':[], 'price':[], 'made_in':[], 'clothes_care':[], 'brand':[]}

def display_all_products():
    """
    Scroll down page to load more articles
    :param : () 
    :return: () 
    """
    for scroll in range(1):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
    return

def get_info_from_links(links, driver, group, category):
    """
    Obtain all the information provided by each link and added to the global dictionary
    :param : 
        links (list): links with the article data
        driver (obj): driver used por web scraping
        group (str) : Group correspoding to the link
        category (str) : Category correspoding to the link
    :return: ()
    """
    global dataset_headers
    global data_dict
    for href in links:
        driver.get(href)
        data_list = get_data(driver, group, category)
        if len(data_list) > 2:
            for key in range(11):
                data_dict[dataset_headers[key]].append(data_list[key])
    return

def go_to_group_section(driver, differential_code):
    """
    Access to the group section
    :param : 
        driver (obj): driver used por web scraping
        differential_code (int): Number corresondig to the group (1,2 or 3)
    :return: ()
    """
    xpath = '/html/body/div[1]/div[1]/div[1]/div/div/aside/div/nav/div/ul/li['+ str(differential_code) +']/a'
    open_group = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,xpath)))
    sleep(3)
    open_group.click()
    return


def get_clothes_links(driver, xpath_num1, xpath_num2, xpath_num3):
    """
    Obtain all the links acordint to the multiple clothes available
    :param : 
        driver (obj): driver used por web scraping
        xpath_num1 (int) : Number corresondig to the group (1,2 or 3)
        xpath_num1 (int) : Number corresondig to the section (1,2 or 3)
        xpath_num3 (int) : Number corresondig to the subsection (1,2 or 3)
    :return: 
        links (list) : list with all the links detected
    """
    xpath = '/html/body/div[1]/div[1]/div[1]/div/div/aside/div/nav/div/ul/li['+str(xpath_num1)+']/ul/li['+ str(xpath_num2)+']/ul/li['+str(xpath_num3)+']/a'
    open_type_clothes = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,xpath)))
    sleep(3)
    open_type_clothes.click()
    display_all_products()
    products = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.product-link')))
    link_products = [product.get_attribute('href') for product in products]
    links = list(set(link_products))
    return links

def desplegable_secciones(driver, group, category, first = False):
    """
    Steps to follow to get the information related to the group and category
    :param : 
        driver (obj): driver used por web scraping
        group (str) : Group to study
        category (str) : Category to study
        first (boolean) : First iteration to the website (False by default)
        
    :return: 
        first (boolean) : Iteration is not the first. Always returns False
    """
    # Open Zara mian site
    urlZaraPage = 'https://www.zara.com/es/'
    driver.get(urlZaraPage)
    if first == True:
        # Accept Cookies to navegate through the page if it is the first access time
        cookie = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'onetrust-accept-btn-handler')))
        sleep(3)
        cookie.click()
        first = False
    # Display group options
    group_list = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.layout-header__mobile-action layout-header__mobile-action--menu'.replace(' ','.'))))
    sleep(3)
    group_list.click()
    if group == 'Mujer':
        # Go through women clothes
        go_to_group_section(driver, 1)
        if category == 'Camisetas':
            links = get_clothes_links(driver,1,3,6)
        elif category == 'Camisa':
            links = get_clothes_links(driver,1,3,4)
        elif category == 'Jeans':
            links = get_clothes_links(driver,1,3,10)
        else:
            links = get_clothes_links(driver,1,3,9)
        get_info_from_links(links, driver, group, category)
            
    elif group == 'Hombre':
        # Go through men clothes
        go_to_group_section(driver, 2)
        if category == 'Camisetas':
            links = get_clothes_links(driver,2,3,8)
        elif category == 'Camisa':
            links = get_clothes_links(driver,2,3,7)
        elif category == 'Jeans':
            links = get_clothes_links(driver,2,3,12)
        else:
            links = get_clothes_links(driver,2,3,13)
        get_info_from_links(links, driver, group, category)
    else:
        go_to_group_section(driver, 3)
        # Go to children group
        if group == 'Niño':
            # Go to boys group
            go_to_group_section(driver, '3]/ul/li[2')
            if category == 'Camisetas':
                links = get_clothes_links(driver,3,2,7)
            elif category == 'Camisa':
                links = get_clothes_links(driver,3,2,8)
            elif category == 'Jeans':
                links = get_clothes_links(driver,3,2,13)
            else:
                links = get_clothes_links(driver,3,2,12)
            get_info_from_links(links, driver, group, category)
        else:
            go_to_group_section(driver, '3]/ul/li[1')
            # Go to girls group
            if category == 'Camisetas':
                links = get_clothes_links(driver,3,1,8)
            elif category == 'Camisa':
                links = get_clothes_links(driver,3,1,9)
            elif category == 'Jeans':
                links = get_clothes_links(driver,3,1,14)
            else:
                links = get_clothes_links(driver,3,1,13)
            get_info_from_links(links, driver, group, category)

    return first




# Navegation options and driver path
options = webdriver.ChromeOptions()
options.add_argument('--headless') #background task; don't open a window
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

# Define groups and categories
group = ['Mujer','Hombre', 'Niño', 'Niña']
category = ['Camisetas', 'Camisa', 'Jeans', 'Pantalones']
first = True
for gender in group:
    for type_clothes in category:
        first = desplegable_secciones(driver, gender, type_clothes, first)

# Create dataset and csv
df = pd.DataFrame.from_dict(data_dict)
df.to_csv('datasetZara.csv')
