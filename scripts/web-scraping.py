from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

import os
import shutil

# download options
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": "/home/marcosvn/Documents/intuitive-care/task1_files", # download directory
    "download.prompt_for_download": False, # auto download file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True # won't show pdf on chorme
})
driver = webdriver.Chrome(options=options)

def accept_cookies():
    acc_cookies = driver.find_element('xpath', '/html/body/div[6]/div/div/div/div/div[2]/button[3]')
    acc_cookies.click()

def donwload_pdfs():
    # make files directory
    dir_name = '/home/marcosvn/Documents/intuitive-care/task1_files'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # move to links
    action = ActionChains(driver)
    action.move_to_element(driver.find_element('xpath', '//*[@id="parent-fieldname-text"]/p[15]/a')).perform()
    time.sleep(2)

    # download each file
    for i in range(11, 16):
        curr_anx = driver.find_element('xpath', '//*[@id="parent-fieldname-text"]/p[{index}]/a'.format(index=i))
        curr_anx.click()
        time.sleep(2)

    # zip folder
    shutil.make_archive('task1_files', 'zip', dir_name)
    # delete task1_files - leaving only the .zip file
    shutil.rmtree(dir_name)

driver.get('https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude')
accept_cookies()
donwload_pdfs()

driver.quit()