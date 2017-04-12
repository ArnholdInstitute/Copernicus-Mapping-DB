#!/bin/bash

URL=http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip

if [ ! -f countries.zip ]; then
	wget $URL -O countries.zip
fi

if [ ! -f ne_50m_admin_0_countries.shp ]; then
	unzip countries.zip
fi

shp2pgsql -s 4326 -D -I -d ne_50m_admin_0_countries.shp countries | psql copernicus