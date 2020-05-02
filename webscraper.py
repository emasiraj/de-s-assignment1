from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pdb
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
url = 'https://www.google.com/travel/hotels/entity/CgsI6-Ga5pH2k4GSARAB/reviews?g2lb=2502548%2C4258168%2C4260007%2C4270442%2C4274032%2C4291318%2C4305595%2C4306835%2C4308226%2C4317915%2C4328159%2C4329288%2C4333265%2C4357967%2C4366684%2C4366858%2C4367952%2C4369397%2C4370794%2C4373848%2C4270859%2C4284970%2C4291517%2C4316256&hl=en&gl=nl&un=1&rp=EOvhmuaR9pOBkgEQ6-Ga5pH2k4GSATgCQABIAQ&ictx=1&sa=X&hrf=IgNFVVIqFgoHCOQPEAUYExIHCOQPEAUYFBgBKACCASUweDQ3N2VhZTIxNTA0NmZkYjc6MHg5MjAyNGZiMTFjYzZiMGVimgEnGiUweDQ3N2VhZTIxNTA0NmZkYjc6MHg5MjAyNGZiMTFjYzZiMGVi'
driver.get(url)

time.sleep(10)
for x in range(11): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"), 
    time.sleep(2)

listOfReviews = [review.text for review in driver.find_elements_by_class_name('kVathc')]
df = pd.DataFrame(listOfReviews, columns=['Review'])
pdb.set_trace()
df.to_csv('scrapedDataframe.csv')


