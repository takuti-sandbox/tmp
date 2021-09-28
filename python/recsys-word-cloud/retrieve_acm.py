from selenium import webdriver
import time

url = 'https://dl.acm.org/doi/proceedings/10.1145/3460231'
driver = webdriver.Chrome()
driver.get(url)

time.sleep(1)

elems = driver.find_elements_by_xpath("//a[contains(@class, 'section__title') and (@aria-expanded='false')]")

for e in elems:
    print(e)
    e.click()
    time.sleep(1)

elems = driver.find_elements_by_xpath("//a[ancestor::h5[contains(@class, 'issue-item__title')]]")
for e in elems:
    print(e.get_attribute('href'))

driver.quit()
