#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import pdb
import pandas
from time import sleep
import requests

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

def download(url, cookies):
	formData = {}
	inputs = driver.find_elements_by_xpath('//div[contains(@class, "region-content")]//form//input')
	for inp in inputs:
		formData[inp.get_attribute('name')] = inp.get_attribute('value')

	local_filename = '../files/' + url.split('/')[-1]
	print('Downloading %s' % local_filename)
	r = requests.post(url, cookies=cookies, data=formData)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return 

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

		all_cookies = driver.get_cookies()
		cookies = {}
		for s_cookie in all_cookies:
			cookies[s_cookie['name']] = s_cookie['value']

		download(base+zl, cookies)
