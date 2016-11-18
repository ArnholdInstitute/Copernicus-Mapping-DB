#!/usr/bin/env python

import glob 
from subprocess import check_output
import pdb
import os
import sys

if not(os.path.exists('json-files')):
	os.mkdir('json-files')

if not(os.path.exists('unzipped')):
	os.mkdir('unzipped')

# unzip everything
for z in glob.glob('files/*.zip'):
	base = os.path.basename(z)
	if not(os.path.exists('unzipped/' + base)):
		check_output(['cp', z, 'unzipped'])
		os.chdir('unzipped')
		check_output(['unzip', '-o', base])
		os.chdir('../')

# convert to geojson
for shp in glob.glob('unzipped/*.shp'):
	d = 'json-files'
	base = os.path.basename(shp)
	s = os.path.splitext(base)
	if not(os.path.exists(d + '/' + s[0] + '.json')):
		check_output(['ogr2ogr', '-F', 'GeoJSON', d + '/' + s[0] + '.json', shp, '-t_srs', 'epsg:4326'])

types = [
	'crisis_information_point_grading',
	'general_information_poly',
	'hydrography_line_grading',
	'physiography_line',
	'settlements_point_grading',
	'transportation_line_grading'
]

cmd='geojson2postgres'

script = open('script.sql', 'w')

# generate the script to load data into Postgres
for ty in types:
	files = glob.glob('json-files/*%s.json' % ty)
	output = check_output([cmd, files[0], '--create', '--tablename', ty])
	script.write(output)
	for file in files[1:]:
		output = check_output([cmd, file, '--tablename', ty])
		script.write(output)

