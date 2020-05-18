from aloe import step, after
from selenium import webdriver
import time

driver = webdriver.Chrome()

@after.each_step
def wait_for_page_to_load(step):
    time.sleep(3)
    

@after.each_feature
def close_browser(step):
    driver.close()

@step('I enter the url (.*) into my browser')
def enter_url(step, url):
    driver.get(url)

@step('I see the title (.*) in the title')
def verify_title(step, title):
    assert title in driver.title

@step('I see there are (.*) log entries by (.*)')
def verify_log_entries(step, amount, author):
    log_table = driver.find_element_by_css_selector('body > div > div.p4 > div > div.w-75 > table > tbody')
    log_entries = log_table.find_elements_by_tag_name('tr')
    assert len(log_entries) == int(amount)

@step('I click on the first log entry')    
def click_first_log_entry(step):
    first_log = driver.find_element_by_css_selector('#row1')
    first_log.click()

@step('I see the first log is written by (.*)')
def verify_log_written_by(step, written_by):
    who_wrote_this = driver.find_element_by_css_selector('#post1 > div.w-75.mv1.ph1').text
    assert written_by in who_wrote_this

