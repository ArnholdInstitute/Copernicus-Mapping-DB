#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import pdb
import pandas
from time import sleep

driver = webdriver.Chrome()

def dump():
	soup = BeautifulSoup(driver.page_source, "html.parser")
	open('out.html', 'w').write(soup.prettify().encode('utf-8'))
	return soup


base = 'http://emergency.copernicus.eu'

driver.get('http://emergency.copernicus.eu/mapping/list-of-activations-rapid')

soup = BeautifulSoup(driver.page_source, "html.parser")
table = soup.find('table', {'class' : 'views-table'})

head = table.findAll('th')
columns = map(lambda x: x.get_text().strip(), head)
rows = map(lambda x: list(x.findAll('td')), table.findAll('tr'))


df = pandas.DataFrame(filter(lambda x: len(x) != 0, rows), columns = columns)

for link in df['Title'].apply(lambda x: x.find('a').attrs['href']):
	driver.get(base + link + '/GRADING/ALL')

	soup = BeautifulSoup(driver.page_source, "html.parser")

	zipLinks = soup.findAll('div', {'class' : 'views-field-field-component-file-vectors'})
	zipLinks = map(lambda n: n.find('a').attrs['href'], zipLinks)

	for zl in zipLinks:
		driver.get(base + zl)
		soup = dump()
		confirmation = driver.find_element_by_name('confirmation')
		confirmation.send_keys(True)
		confirmation.click()
		submit = driver.find_element_by_id('edit-submit')
		submit.click()
		sleep(1) #Sleep for a second so as to not overload their server
