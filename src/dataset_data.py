import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime


def get_id(driver):
    """
    Get id information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        id_ (str) :  id information
    """
    try:
        id_ = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="theme-modal-container"]/div/div/div/div/div[2]/div/p[1]/span[2]'))).text
        return str(id_)
    except:
        return 'NULL'


def get_num_images (driver):
    """
    Get number of images information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        num_images (str) :  number of images information
    """
    return str(len(driver.find_elements_by_xpath('.//button[@class="product-detail-images-thumbnails__thumbnail-wrapper"]')))


def get_size(driver):
    """
    Get size information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        size (str) :  size information
    """
    try: 
        size = [ elem.text for elem in driver.find_elements_by_xpath('.//span[@class="product-size-info__main-label"]')]
        return str(size[0] + '-' + size[-1])
    except:
        return 'NULL'


def get_colour(driver):
    """
    Get colour information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        num_colour (str) :  colour information
    """
    try:
        num_colours = str(len(driver.find_elements_by_xpath('.//button[@class="product-detail-color-selector__color-button"]')))
        if num_colours == '0':
            num_colours = 1
        return str(num_colours)
    except:
        return 'NULL'


def get_season():
    """
    Get season information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        season (str) :  season information
    """
    try:
        date = datetime.now()
        if date.month < 7:
            season = 'Primavera-Verano'
        else:
            season = 'Otoño-Invierno'
        return season
    except:
        return 'NULL'
     

def get_price(driver):
    """
    Get price information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        price (str) :  price information
    """
    try:
        price = driver.find_element_by_xpath('.//span[@class="price__amount"]').text
        return str(price.split(' ')[0])
    except:
        return 'NULL'


def get_made_in(driver):
    """
    Get articles made in origin information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        datdescription_textaset_row (str) : articles made in origin information
    """
    try:
        description_text = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div/div/div[2]/section[1]/div/div[1]/p'))).text
        return str(description_text.split(' ')[-1])
    except:
        return 'NULL'


def get_temp_max_washing_and_spin(driver):
    """
    Get washing machine properties information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        temp_washing_spin (str) :  washing machine properties information
    """
    try:
        temp_washing_spin = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="theme-modal-container"]/div/div/div/div/div[2]/section[3]/div/div[1]/ul/li[1]/span'))).text
        return str(temp_washing_spin)
    except:
        return 'NULL', 'NULL'


def get_whitening(driver):
    """
    Get whitening properties information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        whitening (str) : whitening properties information
    """
    try:
        whitening = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="theme-modal-container"]/div/div/div/div/div[2]/section[3]/div/div[1]/ul/li[2]/span'))).text
        return str(whitening)
    except:
        return 'NULL'


def get_temp_max_iron(driver):
    """
    Get iron properties information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        iron (str) : iron properties information
    """
    try:
        iron = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="theme-modal-container"]/div/div/div/div/div[2]/section[3]/div/div[1]/ul/li[3]/span'))).text
        return str(iron)
    except:
        return 'NULL'


def get_dry_wash(driver):
    """
    Get dry wash properties information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        dry_wash (str) : dry wash properties information
    """
    try:
        dry_wash = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="theme-modal-container"]/div/div/div/div/div[2]/section[3]/div/div[1]/ul/li[4]/span'))).text
        return str(dry_wash)
    except:
        return 'NULL'


def get_drying_machine(driver):
    """
    Get drying machine properties information
    :param : 
        driver (obj): driver used por web scraping
    :return: 
        dry_machine (str) : drying machine properties information
    """
    try:
        dry_machine = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="theme-modal-container"]/div/div/div/div/div[2]/section[3]/div/div[1]/ul/li[5]/span'))).text
        return str(dry_machine)
    except:
        return 'NULL'


def get_data(driver, group, category):
    """
    Obtain article infomration
    :param : 
        driver (obj): driver used por web scraping
        group (str) : Group to study
        category (str) : Category to study
    :return: 
        dataset_row (list) : list with the data to add to the final dataframe
    """
    images = get_num_images(driver)
    size = get_size(driver)
    colour = get_colour(driver)
    season = get_season()
    price = get_price(driver)
    try:
        origin_materials_section = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'.//button[@class="product-detail-actions__action-button"]')))
        origin_materials_section.click()
        id_ = get_id(driver)
        made_in = get_made_in(driver)
        temp_washing_spin = get_temp_max_washing_and_spin(driver)
        whitening = get_whitening(driver)
        temp_iron = get_temp_max_iron(driver)
        dry_wash = get_dry_wash(driver)
        drying_machine = get_drying_machine(driver)
        clothes_care = temp_washing_spin +' - '+whitening+' - '+temp_iron+' - '+dry_wash+' - '+drying_machine
    except:
        id_ = 'NULL'
        made_in = 'NULL'
        temp_washing_spin = 'NULL'
        whitening = 'NULL'
        temp_iron = 'NULL'
        dry_wash = 'NULL'
        drying_machine = 'NULL'
        clothes_care = temp_washing_spin +' - '+whitening+' - '+temp_iron+' - '+dry_wash+' - '+drying_machine
    dataset_row = [id_, group, category, images, size, colour, season, price, made_in, clothes_care, 'Zara']
    return dataset_row